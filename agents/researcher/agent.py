#!/usr/bin/env python3
"""
Researcher Agent (Vertical A - ProQSmart)
Role: Keyword/trend discovery + competitor analysis
Tools: DataForSEO API, SerpBear API, Neo4j KG
"""

import os
import json
import sys
import requests
from base64 import b64encode
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from researcher.mock_data import get_mock_keyword_data

class ResearcherAgent:
    def __init__(self, use_mock_data: bool = False):
        # DataForSEO credentials
        self.dataforseo_email = os.getenv('DATAFORSEO_EMAIL', 'vishal@proqsmart.com')
        self.dataforseo_password = os.getenv('DATAFORSEO_PASSWORD', 'a25b69e4ad3fbbb2')
        self.dataforseo_base = 'https://api.dataforseo.com/v3'
        
        # SerpBear credentials
        self.serpbear_key = os.getenv('SERPBEAR_API_KEY', '4UtFVs80VWZlK4Tq1B0D51eDQPJ0IJiilYGcdQj5')
        self.serpbear_base = 'https://serpbear.com/api'
        
        # Neo4j credentials
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'Agentic2026SecurePass')
        
        # Workspace
        self.workspace = os.getenv('OPENCLAW_WORKSPACE', '/root/.openclaw/workspace-vertical-a')
        
        # Use mock data flag (for testing when API not available)
        self.use_mock_data = use_mock_data
        
        # Auth headers
        auth_string = f"{self.dataforseo_email}:{self.dataforseo_password}"
        self.dataforseo_headers = {
            'Authorization': f'Basic {b64encode(auth_string.encode()).decode()}',
            'Content-Type': 'application/json'
        }
    
    def get_keyword_suggestions(self, seed_keywords: List[str], location_code: int = 2840) -> List[Dict]:
        """Get keyword suggestions from DataForSEO or mock data"""
        
        print(f"🔍 Getting keyword suggestions for: {seed_keywords}")
        
        # Use mock data for now (API needs account activation)
        if self.use_mock_data:
            print("   ℹ️ Using mock data (DataForSEO API needs activation)")
            mock_data = get_mock_keyword_data()
            suggestions = mock_data['suggestions']
            print(f"   ✓ Loaded {len(suggestions)} mock keyword suggestions")
            return suggestions
        
        # Live API call (commented out until API is activated)
        payload = [{
            'keywords': seed_keywords,
            'location_code': location_code,
            'language_code': 'en',
            'search_volume_min': 100
        }]
        
        response = requests.post(
            f'{self.dataforseo_base}/keywords_data/google/keywords/suggestions',
            headers=self.dataforseo_headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('tasks') and len(data['tasks']) > 0:
                results = data['tasks'][0].get('result', [])
                print(f"   ✓ Found {len(results)} keyword suggestions")
                return results
            else:
                print("   ⚠ No results returned")
                return []
        else:
            print(f"   ❌ DataForSEO API error: {response.text}")
            print("   ℹ️ Falling back to mock data")
            mock_data = get_mock_keyword_data()
            return mock_data['suggestions']
    
    def get_keyword_difficulty(self, keywords: List[str]) -> List[Dict]:
        """Get keyword difficulty scores"""
        
        print(f"📊 Getting difficulty scores for {len(keywords)} keywords...")
        
        if self.use_mock_data:
            mock_data = get_mock_keyword_data()
            difficulty = mock_data['difficulty']
            print(f"   ✓ Loaded difficulty for {len(difficulty)} keywords")
            return difficulty
        
        payload = [{'keywords': keywords}]
        
        response = requests.post(
            f'{self.dataforseo_base}/keywords_data/google/keywords/difficulty',
            headers=self.dataforseo_headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('tasks') and len(data['tasks']) > 0:
                results = data['tasks'][0].get('result', [])
                print(f"   ✓ Got difficulty for {len(results)} keywords")
                return results
            else:
                return []
        else:
            print(f"   ❌ DataForSEO error: {response.text}")
            mock_data = get_mock_keyword_data()
            return mock_data['difficulty']
    
    def store_in_neo4j(self, keywords: List[Dict], difficulty: List[Dict]) -> int:
        """Store keyword research results in Neo4j"""
        
        print(f"💾 Storing {len(keywords)} keywords in Neo4j...")
        
        count = 0
        for kw in keywords:
            term = kw.get('keyword', '')
            volume = kw.get('search_volume', 0)
            
            if not term:
                continue
            
            # Find matching difficulty
            diff_score = 0
            for d in difficulty:
                if d.get('keyword') == term:
                    diff_score = d.get('keyword_difficulty', 0)
                    break
            
            # Escape single quotes for Cypher
            term_escaped = term.replace("'", "\\'")
            
            # Create Cypher query
            cypher = f"""
MERGE (k:Keyword {{term: '{term_escaped}', vertical: 'A'}})
ON CREATE SET k.volume = {volume},
              k.difficulty = {diff_score},
              k.intent = 'commercial',
              k.createdAt = datetime()
ON MATCH SET k.volume = {volume},
             k.difficulty = {diff_score}
"""
            
            # Execute via docker
            import subprocess
            result = subprocess.run(
                ['docker', 'exec', '-i', 'agentic-pipeline-neo4j',
                 'bin/cypher-shell', '-u', self.neo4j_user,
                 '-p', self.neo4j_password],
                input=cypher.encode(),
                capture_output=True
            )
            
            if result.returncode == 0:
                count += 1
            else:
                print(f"   ⚠ Failed to store '{term}': {result.stderr.decode()[:100]}")
        
        print(f"   ✓ Stored {count}/{len(keywords)} keywords in Neo4j")
        return count
    
    def research_keywords(self, seed_keywords: List[str]) -> Dict:
        """Full keyword research workflow"""
        
        print("=" * 60)
        print("🚀 Starting Keyword Research")
        print("=" * 60)
        
        # Step 1: Get suggestions
        suggestions = self.get_keyword_suggestions(seed_keywords)
        
        # Step 2: Get difficulty scores
        all_keywords = [kw.get('keyword', '') for kw in suggestions]
        difficulty = self.get_keyword_difficulty(all_keywords)
        
        # Step 3: Store in Neo4j
        stored_count = self.store_in_neo4j(suggestions, difficulty)
        
        # Step 4: Analyze results
        primary = [k for k in suggestions if k.get('search_volume', 0) > 1000]
        long_tail = [k for k in suggestions if 100 < k.get('search_volume', 0) <= 1000]
        
        print("\n" + "=" * 60)
        print("✅ Keyword Research Complete")
        print("=" * 60)
        print(f"   Total keywords: {len(suggestions)}")
        print(f"   Primary (>1000/mo): {len(primary)}")
        print(f"   Long-tail (100-1000/mo): {len(long_tail)}")
        print(f"   Stored in Neo4j: {stored_count}")
        
        # Save to workspace
        os.makedirs(f'{self.workspace}/research', exist_ok=True)
        with open(f'{self.workspace}/research/keyword-strategy.json', 'w') as f:
            json.dump({
                'seed_keywords': seed_keywords,
                'total_keywords': len(suggestions),
                'primary_keywords': primary,
                'long_tail_keywords': long_tail,
                'all_keywords': suggestions,
                'difficulty': difficulty,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2, default=str)
        
        print(f"   💾 Saved to: {self.workspace}/research/keyword-strategy.json")
        
        return {
            'success': True,
            'total_keywords': len(suggestions),
            'primary_count': len(primary),
            'long_tail_count': len(long_tail),
            'stored_in_neo4j': stored_count,
            'primary_keywords': primary,
            'long_tail_keywords': long_tail
        }

# Main execution
if __name__ == '__main__':
    # Use mock data for testing (set to False when DataForSEO API is activated)
    use_mock = True
    
    researcher = ResearcherAgent(use_mock_data=use_mock)
    
    # Research keywords for ProQSmart
    seed_keywords = [
        'AI procurement software',
        'manufacturing automation',
        'procurement automation'
    ]
    
    result = researcher.research_keywords(seed_keywords)
    print("\n" + json.dumps(result, indent=2, default=str))
