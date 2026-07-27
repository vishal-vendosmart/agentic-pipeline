#!/usr/bin/env python3
"""
Researcher Agent (Vertical A - ProQSmart)
Role: Keyword/trend discovery + competitor analysis
Tools: DataForSEO API, SerpBear API, Neo4j KG
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_data import get_mock_keyword_data

# Rest of imports
import json
import requests
from base64 import b64encode
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

class ResearcherAgent:
    def __init__(self, use_mock_data: bool = True):
        self.dataforseo_email = os.getenv('DATAFORSEO_EMAIL', 'vishal@proqsmart.com')
        self.dataforseo_password = os.getenv('DATAFORSEO_PASSWORD', 'a25b69e4ad3fbbb2')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'Agentic2026SecurePass')
        self.workspace = os.getenv('OPENCLAW_WORKSPACE', '/root/.openclaw-pm/workspace-vertical-a')
        self.use_mock_data = use_mock_data
    
    def research_keywords(self, seed_keywords: List[str]) -> Dict:
        """Full keyword research workflow"""
        print(f"🔍 Researching keywords: {seed_keywords}")
        
        # Get mock data
        mock_data = get_mock_keyword_data()
        suggestions = mock_data['suggestions']
        difficulty = mock_data['difficulty']
        
        # Store in Neo4j
        count = 0
        for kw in suggestions:
            term = kw.get('keyword', '')
            volume = kw.get('search_volume', 0)
            if not term:
                continue
            
            diff_score = next((d.get('keyword_difficulty', 0) for d in difficulty if d.get('keyword') == term), 0)
            
            cypher = f"""
MERGE (k:Keyword {{term: '{term.replace("'", "''")}', vertical: 'A'}})
ON CREATE SET k.volume = {volume}, k.difficulty = {diff_score}, k.intent = 'commercial', k.createdAt = datetime()
"""
            result = subprocess.run(
                ['docker', 'exec', '-i', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
                 '-u', self.neo4j_user, '-p', self.neo4j_password],
                input=cypher.encode(), capture_output=True
            )
            if result.returncode == 0:
                count += 1
        
        print(f"✅ Stored {count} keywords in Neo4j")
        
        # Save to workspace
        os.makedirs(f'{self.workspace}/research', exist_ok=True)
        with open(f'{self.workspace}/research/keyword-strategy.json', 'w') as f:
            json.dump({'keywords': suggestions, 'difficulty': difficulty}, f, indent=2)
        
        return {'success': True, 'total_keywords': len(suggestions), 'stored_in_neo4j': count}

if __name__ == '__main__':
    agent = ResearcherAgent()
    result = agent.research_keywords(['AI procurement software'])
    print(json.dumps(result, indent=2))
