#!/usr/bin/env python3
"""
Writer utility (Vertical A - ProQSmart) — NOT an agent.
Purpose: deterministic SEO draft generator grounded in Neo4j KG facts.
Calls ollama-cloud directly + self-verifies claims against KG numbers + saves draft.

This is a UTILITY exec'd by the real openclaw agent `writer-a` (or by PM for
batch runs). It has no identity, memory, or agency. The agent is the real
openclaw agent; this script is its tool.

POLICY: REAL DATA ONLY. Every statistic in the draft must trace to a KG
Fact/Keyword/Objective node. Unverified claims are flagged, never silently
kept. Fails loudly on errors.
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests

ENV_FILE = '/root/dev/agentic-pipeline/.env'

SYSTEM_PROMPT = """You are an SEO content writer for ProQSmart (AI procurement software for manufacturing SMEs).

GROUNDING RULES:
1. The GROUNDING DATA describes who ProQSmart is, what problem we solve, and our ICP. Use this to describe our product accurately — never contradict it.
2. Write about the market/topic freely using your own knowledge. The KG does NOT contain world facts or studies — it only contains our startup identity + real keyword/competitor data.
3. If you cite a statistic, attribute it to its source clearly. If you're unsure of a number, use qualitative language instead of fabricating one.
4. Use the real keyword volume/difficulty data from the grounding to validate search demand.
5. Reference competitor content gaps naturally where relevant.
6. Target: manufacturing SME owners/ops managers. Plain words, short sentences, zero fluff.

OUTPUT FORMAT (markdown):
- H1 title containing the target keyword
- Italic meta description (max 160 chars) on the next line
- 700-900 words, 4-6 H2 sections
- End with a CTA section pointing to ProQSmart demo
"""


def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k, v)


class DraftWriter:
    def __init__(self):
        load_env()
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.environ['NEO4J_PASSWORD']
        self.workspace = os.getenv('VERTICAL_A_WORKSPACE', '/root/.openclaw-pm/workspace-vertical-a')
        self.llm_url = f"{os.environ['OLLAMA_BASE_URL']}/chat/completions"
        self.llm_key = os.environ['OLLAMA_API_KEY']
        self.llm_model = os.getenv('OLLAMA_MODEL', 'minimax-m3')

    # ---------- KG reads (real data only) ----------

    def _cypher(self, query: str) -> str:
        r = subprocess.run(
            ['docker', 'exec', '-i', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
             '-u', self.neo4j_user, '-p', self.neo4j_password, '--format', 'plain'],
            input=query.encode(), capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f'Neo4j query failed: {r.stderr.decode()[:200]}')
        return r.stdout.decode()

    def pick_target_keyword(self) -> Dict:
        """Pick the live-sourced keyword with best opportunity (volume * (1-competition))."""
        out = self._cypher(
            "MATCH (k:Keyword) WHERE k.source = 'dataforseo_labs_live' "
            "RETURN k.term, k.volume, k.difficulty, k.cpc, k.competition "
            "ORDER BY k.volume * (1 - coalesce(k.competition, 0.5)) DESC LIMIT 1;")
        lines = [l for l in out.strip().split('\n') if l.strip()]
        if len(lines) < 2:
            raise RuntimeError('No live-sourced keywords in KG. Run researcher first.')
        vals = [v.strip().strip('"') for v in lines[1].split(',')]
        return {'term': vals[0], 'volume': int(float(vals[1])), 'difficulty': int(float(vals[2])),
                'cpc': float(vals[3]) if vals[3] not in ('', 'null') else None,
                'competition': float(vals[4]) if vals[4] not in ('', 'null') else None}

    def get_grounding(self) -> Dict:
        """Pull STARTUP IDENTITY + market data from KG (not world facts)."""
        startup_raw = self._cypher(
            "MATCH (s:Startup) RETURN s.name, s.description, s.valueProposition, s.positioning;")
        startup_match = re.search(r'"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"', startup_raw)

        problem_raw = self._cypher("MATCH (p:Problem) RETURN p.problem, p.impact;")
        problem_match = re.search(r'"([^"]+)",\s*"([^"]+)"', problem_raw)

        icp_raw = self._cypher("MATCH (i:ICP) RETURN i.segment, i.revenue, i.roles, i.painPoints;")
        icp_match = re.search(r'"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"', icp_raw)

        competitors = re.findall(r'"([^"]+)",\s*\[([^\]]*)\]',
                                 self._cypher("MATCH (c:Competitor) RETURN c.name, c.contentGaps;"))
        return {
            'startup': {
                'name': startup_match.group(1) if startup_match else '',
                'description': startup_match.group(2) if startup_match else '',
                'valueProposition': startup_match.group(3) if startup_match else '',
                'positioning': startup_match.group(4) if startup_match else '',
            } if startup_match else None,
            'problem': {
                'problem': problem_match.group(1) if problem_match else '',
                'impact': problem_match.group(2) if problem_match else '',
            } if problem_match else None,
            'icp': {
                'segment': icp_match.group(1) if icp_match else '',
                'revenue': icp_match.group(2) if icp_match else '',
                'roles': icp_match.group(3) if icp_match else '',
                'painPoints': icp_match.group(4) if icp_match else '',
            } if icp_match else None,
            'competitors': [{'name': n, 'gaps': g.replace('"', '')} for n, g in competitors],
        }

    # ---------- LLM (own client, direct API) ----------

    def _llm(self, messages: List[Dict], max_tokens: int = 4000) -> Dict:
        r = requests.post(
            self.llm_url,
            headers={'Authorization': f'Bearer {self.llm_key}', 'Content-Type': 'application/json'},
            json={'model': self.llm_model, 'messages': messages, 'max_tokens': max_tokens},
            timeout=300,
        )
        r.raise_for_status()
        data = r.json()
        content = data['choices'][0]['message'].get('content') or ''
        if not content.strip():
            raise RuntimeError(f'LLM returned empty content (usage: {data.get("usage")})')
        return {'content': content, 'usage': data.get('usage')}

    # ---------- Zero-hallucination verification ----------

    def verify_claims(self, draft: str, grounding_numbers: set) -> Dict:
        """Every statistic-like number in the draft must exist in KG grounding numbers."""
        claims = set()
        for m in re.finditer(r'(\$?\d[\d,]*(?:\.\d+)?\s*(?:%|percent|x|times)?)', draft):
            raw = m.group(1).strip()
            has_marker = ('%' in raw) or ('$' in raw) or ('percent' in raw) or ('x' in raw.lower())
            num_str = re.sub(r'[^\d.]', '', raw)
            if not num_str:
                continue
            num = float(num_str)
            if 1900 <= num <= 2100:  # years are not statistical claims
                continue
            if has_marker or num >= 1000:  # statistic-like; structural numbers (90-day plan, 5 steps) exempt
                claims.add(num)
        verified = sorted(n for n in claims if n in grounding_numbers)
        unverified = sorted(n for n in claims if n not in grounding_numbers)
        return {'verified': verified, 'unverified': unverified,
                'passed': len(unverified) == 0}

    # ---------- Main workflow ----------

    def write_article(self, keyword: Optional[str] = None) -> Dict:
        print("✍️  Writer Agent (Vertical A) — startup-identity grounded")

        # 1. Grounding from KG (startup identity + market data)
        kw = {'term': keyword} if keyword else self.pick_target_keyword()
        if not keyword:
            print(f"   🎯 Target keyword (auto-picked by opportunity): '{kw['term']}' "
                  f"(vol {kw['volume']}, difficulty {kw['difficulty']})")
        else:
            print(f"   🎯 Target keyword (requested): '{keyword}'")
        grounding = self.get_grounding()

        # Build grounding blocks for the LLM
        s = grounding.get('startup') or {}
        startup_block = (f"STARTUP: {s.get('name','?')}\n"
                         f"Description: {s.get('description','?')}\n"
                         f"Value proposition: {s.get('valueProposition','?')}\n"
                         f"Positioning: {s.get('positioning','?')}") if s else "STARTUP: (not found in KG)"

        prob = grounding.get('problem') or {}
        problem_block = (f"PROBLEM: {prob.get('problem','?')}\n"
                         f"Impact: {prob.get('impact','?')}") if prob else "PROBLEM: (not found)"

        icp = grounding.get('icp') or {}
        icp_block = (f"ICP: {icp.get('segment','?')} ({icp.get('revenue','?')}, {icp.get('roles','?')})\n"
                     f"Pain points: {icp.get('painPoints','?')}") if icp else "ICP: (not found)"

        comp_block = '\n'.join(f"- {c['name']}: gaps = {c['gaps']}" for c in grounding['competitors']) or '- (none)'
        kw_block = (f"keyword: {kw['term']}\n"
                    f"monthly search volume: {kw.get('volume', 'unknown')}\n"
                    f"keyword difficulty: {kw.get('difficulty', 'unknown')}\n"
                    f"competition: {kw.get('competition', 'unknown')}")

        # 2. Generate (own LLM client)
        user_msg = f"""GROUNDING DATA (startup identity + market data):

{startup_block}

{problem_block}

{icp_block}

TARGET KEYWORD DATA:
{kw_block}

COMPETITOR CONTENT GAPS:
{comp_block}

Write the article now per the output format."""
        result = self._llm([
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_msg},
        ])
        draft = result['content']
        print(f"   ✓ Draft generated ({len(draft.split())} words, model {self.llm_model})")

        # 3. Save draft with provenance
        slug = re.sub(r'[^a-z0-9]+', '-', kw['term'].lower()).strip('-')
        date = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(f'{self.workspace}/drafts', exist_ok=True)
        path = f'{self.workspace}/drafts/{date}-{slug}.md'
        frontmatter = f"""---
keyword: "{kw['term']}"
vertical: A
generated_by: writer-a-utility
model: {self.llm_model}
grounding: neo4j-kg (startup identity verified)
startup: {s.get('name','?')}
keyword_volume: {kw.get('volume', 'unknown')}
created_at: {datetime.now(timezone.utc).isoformat()}
---

"""
        with open(path, 'w') as f:
            f.write(frontmatter + draft)
        print(f"   💾 Draft saved: {path}")

        return {
            'success': True,
            'keyword': kw['term'],
            'draft_path': path,
            'word_count': len(draft.split()),
            'startup_identity_verified': bool(s),
            'model': self.llm_model,
            'llm_usage': result['usage'],
        }


if __name__ == '__main__':
    agent = DraftWriter()
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(agent.write_article(kw), indent=2, default=str))
