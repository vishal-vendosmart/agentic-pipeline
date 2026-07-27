#!/usr/bin/env python3
"""
Researcher utility (Vertical A - ProQSmart) — NOT an agent.
Purpose: deterministic keyword/trend discovery helper.
Calls DataForSEO Labs (LIVE) + writes Neo4j KG + saves keyword-strategy.json.

This is a UTILITY exec'd by the real openclaw agent `researcher-a` (or by PM
for batch runs). It has no identity, memory, or agency. The agent is the
real openclaw agent; this script is its tool.

Policy: REAL DATA ONLY. No mock/simulated output. Fails loudly on API errors.
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone
from typing import Dict, List
import subprocess

ENV_FILE = '/root/dev/agentic-pipeline/.env'
DFS_BASE = 'https://api.dataforseo.com/v3/dataforseo_labs/google'
LOCATION_CODE = 2840  # United States
LANGUAGE_CODE = 'en'


def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k, v)


class ResearchTool:
    def __init__(self):
        load_env()
        self.dfs_auth = (
            os.environ['DATAFORSEO_EMAIL'],
            os.environ['DATAFORSEO_PASSWORD'],
        )
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.environ['NEO4J_PASSWORD']
        self.workspace = os.getenv('VERTICAL_A_WORKSPACE', '/root/.openclaw-pm/workspace-vertical-a')
        self.total_cost = 0.0

    def _dfs_post(self, endpoint: str, payload: List[Dict]) -> Dict:
        r = requests.post(
            f'{DFS_BASE}/{endpoint}',
            auth=self.dfs_auth,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        if data.get('status_code') != 20000:
            raise RuntimeError(f"DataForSEO error {data.get('status_code')}: {data.get('status_message')}")
        task = (data.get('tasks') or [{}])[0]
        if task.get('status_code') != 20000:
            raise RuntimeError(f"DataForSEO task error {task.get('status_code')}: {task.get('status_message')}")
        self.total_cost += float(task.get('cost') or 0)
        return task

    def get_keyword_suggestions(self, seed: str, limit: int = 20) -> List[Dict]:
        """REAL keyword suggestions from DataForSEO Labs (live)."""
        task = self._dfs_post('keyword_suggestions/live', [{
            'keyword': seed,
            'location_code': LOCATION_CODE,
            'language_code': LANGUAGE_CODE,
            'limit': limit,
            'include_seed_keyword': True,
        }])
        items = ((task.get('result') or [{}])[0]).get('items') or []
        out = []
        for it in items:
            ki = it.get('keyword_info', {}) or {}
            out.append({
                'keyword': it.get('keyword'),
                'search_volume': ki.get('search_volume') or 0,
                'cpc': ki.get('cpc'),
                'competition': ki.get('competition'),
            })
        return [k for k in out if k['keyword']]

    def get_keyword_difficulty(self, keywords: List[str]) -> Dict[str, int]:
        """REAL keyword difficulty from DataForSEO Labs (live)."""
        if not keywords:
            return {}
        task = self._dfs_post('bulk_keyword_difficulty/live', [{
            'keywords': keywords,
            'location_code': LOCATION_CODE,
            'language_code': LANGUAGE_CODE,
        }])
        result = {}
        for r in (task.get('result') or []):
            for it in (r.get('items') or []):
                if it.get('keyword'):
                    result[it['keyword']] = it.get('keyword_difficulty') or 0
        return result

    def _neo4j(self, cypher: str) -> bool:
        result = subprocess.run(
            ['docker', 'exec', '-i', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
             '-u', self.neo4j_user, '-p', self.neo4j_password],
            input=cypher.encode(), capture_output=True
        )
        return result.returncode == 0

    def research_keywords(self, seed_keywords: List[str]) -> Dict:
        """Full keyword research workflow — REAL DataForSEO Labs data only."""
        print(f"🔍 Researching keywords (LIVE DataForSEO): {seed_keywords}")

        # 1. Real suggestions per seed
        suggestions: Dict[str, Dict] = {}
        for seed in seed_keywords:
            for kw in self.get_keyword_suggestions(seed):
                term = kw['keyword']
                if term not in suggestions or kw['search_volume'] > suggestions[term]['search_volume']:
                    suggestions[term] = kw
        keywords = list(suggestions.values())
        print(f"   ✓ {len(keywords)} unique keywords from live API")

        # 2. Real difficulty scores
        difficulty_map = self.get_keyword_difficulty([k['keyword'] for k in keywords])
        print(f"   ✓ difficulty for {len(difficulty_map)} keywords")

        # 3. Store in Neo4j (MERGE: create or refresh real values)
        stored = 0
        for kw in keywords:
            term = kw['keyword'].replace("'", "''")
            volume = int(kw['search_volume'])
            cpc = float(kw['cpc'] or 0)
            competition = float(kw['competition'] or 0)
            diff = int(difficulty_map.get(kw['keyword'], 0))
            cypher = f"""
MERGE (k:Keyword {{term: '{term}', vertical: 'A'}})
ON CREATE SET k.volume = {volume}, k.difficulty = {diff}, k.cpc = {cpc},
              k.competition = {competition}, k.intent = 'commercial',
              k.source = 'dataforseo_labs_live', k.createdAt = datetime()
ON MATCH SET  k.volume = {volume}, k.difficulty = {diff}, k.cpc = {cpc},
              k.competition = {competition}, k.source = 'dataforseo_labs_live',
              k.updatedAt = datetime()
RETURN k.term
"""
            if self._neo4j(cypher):
                stored += 1
        print(f"✅ Stored/updated {stored} keywords in Neo4j (real data)")

        # 4. Save to workspace with provenance
        os.makedirs(f'{self.workspace}/research', exist_ok=True)
        payload = {
            'source': 'dataforseo_labs_live',
            'fetched_at': datetime.now(timezone.utc).isoformat(),
            'seed_keywords': seed_keywords,
            'api_cost_usd': round(self.total_cost, 5),
            'keywords': keywords,
            'difficulty': difficulty_map,
        }
        with open(f'{self.workspace}/research/keyword-strategy.json', 'w') as f:
            json.dump(payload, f, indent=2)

        return {
            'success': True,
            'total_keywords': len(keywords),
            'stored_in_neo4j': stored,
            'source': 'dataforseo_labs_live',
            'api_cost_usd': round(self.total_cost, 5),
        }


if __name__ == '__main__':
    agent = ResearchTool()
    result = agent.research_keywords(['AI procurement software', 'manufacturing automation'])
    print(json.dumps(result, indent=2))
