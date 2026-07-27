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

STRICT GROUNDING RULES:
1. You may ONLY state statistics/numbers that appear in the GROUNDING DATA provided.
2. Every statistic must cite its source inline exactly as given (e.g. "(McKinsey 2025)").
3. Do NOT invent studies, companies, percentages, dollar figures, example amounts, or quotes.
4. Do NOT use illustrative calculations with invented numbers (e.g. "$5M manufacturer saves $1.5M"). Illustrate impact qualitatively instead.
5. You MAY explain concepts, give qualitative advice, and structure arguments freely.
6. Target: manufacturing SME owners/ops managers. Plain words, short sentences, zero fluff.

OUTPUT FORMAT (markdown):
- H1 title containing the target keyword
- Italic meta description (max 160 chars) on the next line
- 700-900 words, 4-6 H2 sections
- Naturally reference the competitor content gaps where relevant
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
        facts = re.findall(r'"([^"]+)",\s*"([^"]+)"',
                           self._cypher("MATCH (f:Fact) WHERE f.verified = true RETURN f.claim, f.source;"))
        competitors = re.findall(r'"([^"]+)",\s*\[([^\]]*)\]',
                                 self._cypher("MATCH (c:Competitor) RETURN c.name, c.contentGaps;"))
        obj_raw = self._cypher("MATCH (o:Objective) RETURN o.title, o.target LIMIT 1;")
        obj = re.search(r'"([^"]+)",\s*(\d+)', obj_raw)
        return {
            'facts': [{'claim': c, 'source': s} for c, s in facts],
            'competitors': [{'name': n, 'gaps': g.replace('"', '')} for n, g in competitors],
            'objective': {'title': obj.group(1), 'target': int(obj.group(2))} if obj else None,
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
        print("✍️  Writer Agent (Vertical A) — independent, KG-grounded")

        # 1. Grounding from KG (real)
        kw = {'term': keyword} if keyword else self.pick_target_keyword()
        if not keyword:
            print(f"   🎯 Target keyword (auto-picked by opportunity): '{kw['term']}' "
                  f"(vol {kw['volume']}, difficulty {kw['difficulty']})")
        else:
            print(f"   🎯 Target keyword (requested): '{keyword}'")
        grounding = self.get_grounding()

        grounding_numbers = set()
        for f in grounding['facts']:
            grounding_numbers.update(float(n) for n in re.findall(r'\d+(?:\.\d+)?', f['claim']))
        if kw.get('volume'):
            grounding_numbers.add(float(kw['volume']))
        if grounding['objective']:
            grounding_numbers.add(float(grounding['objective']['target']))

        facts_block = '\n'.join(f"- {f['claim']} (source: {f['source']})" for f in grounding['facts']) or '- (none)'
        comp_block = '\n'.join(f"- {c['name']}: gaps = {c['gaps']}" for c in grounding['competitors']) or '- (none)'
        kw_block = (f"keyword: {kw['term']}\n"
                    f"monthly search volume: {kw.get('volume', 'unknown')}\n"
                    f"keyword difficulty: {kw.get('difficulty', 'unknown')}\n"
                    f"competition: {kw.get('competition', 'unknown')}")
        obj_block = (f"business objective: {grounding['objective']['title']} "
                     f"(target: {grounding['objective']['target']})" if grounding['objective'] else '')

        # 2. Generate (own LLM client)
        user_msg = f"""GROUNDING DATA (the only facts you may use):

TARGET KEYWORD DATA:
{kw_block}

VERIFIED FACTS (cite inline with source):
{facts_block}

COMPETITOR CONTENT GAPS:
{comp_block}

{obj_block}

Write the article now per the output format."""
        result = self._llm([
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_msg},
        ])
        draft = result['content']
        print(f"   ✓ Draft generated ({len(draft.split())} words, model {self.llm_model})")

        # 3. Zero-hallucination verification (real check)
        check = self.verify_claims(draft, grounding_numbers)
        status = 'verified' if check['passed'] else 'needs_review'
        print(f"   {'✅' if check['passed'] else '⚠️'} Claim verification: "
              f"{len(check['verified'])} verified, {len(check['unverified'])} unverified {check['unverified'] or ''}")

        # 4. Save draft with provenance
        slug = re.sub(r'[^a-z0-9]+', '-', kw['term'].lower()).strip('-')
        date = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(f'{self.workspace}/drafts', exist_ok=True)
        path = f'{self.workspace}/drafts/{date}-{slug}.md'
        frontmatter = f"""---
keyword: "{kw['term']}"
vertical: A
status: {status}
generated_by: hermes-writer-vertical-a (independent agent)
model: {self.llm_model}
grounding: neo4j-kg (facts: {len(grounding['facts'])}, competitors: {len(grounding['competitors'])})
verification: {json.dumps(check)}
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
            'verification': check,
            'status': status,
            'model': self.llm_model,
            'llm_usage': result['usage'],
        }


if __name__ == '__main__':
    agent = DraftWriter()
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(agent.write_article(kw), indent=2, default=str))
