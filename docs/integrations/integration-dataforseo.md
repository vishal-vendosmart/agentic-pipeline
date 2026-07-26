# Integration Specification: DataForSEO

**Service:** DataForSEO API  
**Purpose:** Keyword research, search volume, difficulty data  
**Integration Type:** REST API  
**Cost:** Pay-per-use (~$2.50/month for MVP)  

---

## 1. Overview

DataForSEO provides keyword research data including search volume, difficulty, CPC, and trends. The Researcher agent uses DataForSEO to discover high-value keywords for content targeting.

---

## 2. Setup

### 2.1 Create Account

1. Visit https://dataforseo.com
2. Click "Sign Up" → Create account
3. Verify email address
4. Navigate to Settings → API Credentials
5. Note API email and password (separate from login credentials)
6. Make initial deposit: $1 recommended (5000+ queries)

### 2.2 Configure Environment

```bash
# .env
DATAFORSEO_EMAIL=your-api-email@example.com
DATAFORSEO_PASSWORD=your-api-password
DATAFORSEO_BASE_URL=https://api.dataforseo.com/v3
```

### 2.3 Install Dependencies

```bash
pip install dataforseo-client
```

---

## 3. API Endpoints

### 3.1 Keyword Suggestions

```http
POST /keywords_data/dataforseo/keywords/suggestions
Content-Type: application/json
Authorization: Basic base64(email:password)

{
  "keywords": ["AI procurement software"],
  "location_code": 2840,  # United States
  "language_code": "en",
  "search_volume_min": 100
}
```

**Response:**
```json
{
  "tasks": [
    {
      "result": [
        {
          "keyword": "AI procurement software",
          "location_code": 2840,
          "language_code": "en",
          "search_volume": 2400,
          "cpc": 12.50,
          "competition": 0.45,
          "monthly_searches": [
            {"year": 2026, "month": 7, "search_volume": 2400},
            {"year": 2026, "month": 6, "search_volume": 2350}
          ]
        }
      ]
    }
  ]
}
```

### 3.2 Keyword Difficulty

```http
POST /keywords_data/dataforseo/keywords/difficulty
Content-Type: application/json
Authorization: Basic base64(email:password)

{
  "keywords": ["AI procurement software", "manufacturing automation"]
}
```

**Response:**
```json
{
  "tasks": [
    {
      "result": [
        {
          "keyword": "AI procurement software",
          "keyword_difficulty": 45,
          "serp_features": ["featured_snippet", "people_also_ask"]
        }
      ]
    }
  ]
}
```

### 3.3 Related Keywords

```http
POST /keywords_data/dataforseo/keywords/related
Content-Type: application/json
Authorization: Basic base64(email:password)

{
  "keywords": ["AI procurement"],
  "location_code": 2840,
  "language_code": "en"
}
```

**Response:**
```json
{
  "tasks": [
    {
      "result": [
        {
          "keyword": "AI procurement",
          "related_keywords": [
            {
              "keyword": "procurement automation software",
              "search_volume": 880,
              "competition": 0.38
            },
            {
              "keyword": "AI purchasing system",
              "search_volume": 590,
              "competition": 0.42
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 4. Python Client

### 4.1 DataForSEO Client Class

```python
#!/usr/bin/env python3
"""
DataForSEO API Client
Keyword research and search volume data
"""

import requests
from base64 import b64encode
from typing import Dict, List

class DataForSEOClient:
    def __init__(self, email: str, password: str):
        self.base_url = 'https://api.dataforseo.com/v3'
        auth_string = f"{email}:{password}"
        self.headers = {
            'Authorization': f'Basic {b64encode(auth_string.encode()).decode()}',
            'Content-Type': 'application/json'
        }
    
    def get_keyword_suggestions(self, keywords: List[str], 
                                 location_code: int = 2840,
                                 language_code: str = 'en',
                                 search_volume_min: int = 100) -> List[Dict]:
        """Get keyword suggestions with search volume"""
        
        payload = {
            'keywords': keywords,
            'location_code': location_code,
            'language_code': language_code,
            'search_volume_min': search_volume_min
        }
        
        response = requests.post(
            f'{self.base_url}/keywords_data/dataforseo/keywords/suggestions',
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['tasks'][0]['result']
        else:
            raise Exception(f"DataForSEO API error: {response.text}")
    
    def get_keyword_difficulty(self, keywords: List[str]) -> List[Dict]:
        """Get keyword difficulty scores"""
        
        payload = {'keywords': keywords}
        
        response = requests.post(
            f'{self.base_url}/keywords_data/dataforseo/keywords/difficulty',
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['tasks'][0]['result']
        else:
            raise Exception(f"DataForSEO API error: {response.text}")
    
    def get_related_keywords(self, keywords: List[str],
                              location_code: int = 2840,
                              language_code: str = 'en') -> List[Dict]:
        """Get related keywords"""
        
        payload = {
            'keywords': keywords,
            'location_code': location_code,
            'language_code': language_code
        }
        
        response = requests.post(
            f'{self.base_url}/keywords_data/dataforseo/keywords/related',
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['tasks'][0]['result']
        else:
            raise Exception(f"DataForSEO API error: {response.text}")
    
    def research_keywords(self, seed_keywords: List[str]) -> Dict:
        """Full keyword research workflow"""
        
        print(f"🔍 Researching keywords for: {seed_keywords}")
        
        # Step 1: Get suggestions
        suggestions = self.get_keyword_suggestions(seed_keywords)
        
        # Step 2: Get difficulty
        all_keywords = [k['keyword'] for k in suggestions]
        difficulty = self.get_keyword_difficulty(all_keywords)
        
        # Step 3: Get related keywords
        related = self.get_related_keywords(seed_keywords)
        
        # Combine results
        keyword_data = {}
        for kw in suggestions:
            keyword = kw['keyword']
            keyword_data[keyword] = {
                'search_volume': kw.get('search_volume', 0),
                'cpc': kw.get('cpc', 0),
                'competition': kw.get('competition', 0),
                'difficulty': next(
                    (d['keyword_difficulty'] for d in difficulty 
                     if d['keyword'] == keyword),
                    0
                )
            }
        
        # Analyze
        primary = [k for k, v in keyword_data.items() 
                   if v['search_volume'] > 1000 and v['difficulty'] < 50]
        long_tail = [k for k, v in keyword_data.items() 
                     if v['search_volume'] > 100 and v['search_volume'] <= 1000]
        
        return {
            'success': True,
            'totalKeywords': len(keyword_data),
            'primaryKeywords': primary,
            'longTailKeywords': long_tail,
            'keywordData': keyword_data
        }

# Usage
if __name__ == '__main__':
    import os
    import json
    
    client = DataForSEOClient(
        email=os.getenv('DATAFORSEO_EMAIL'),
        password=os.getenv('DATAFORSEO_PASSWORD')
    )
    
    result = client.research_keywords(['AI procurement software'])
    print(json.dumps(result, indent=2))
```

---

## 5. Error Handling

### 5.1 Authentication Errors

```python
def handle_auth_error(error: Exception):
    """Handle DataForSEO authentication failures"""
    
    if '401' in str(error) or 'unauthorized' in str(error).lower():
        logger.error("DataForSEO API credentials invalid")
        await notify_human("⚠️ DataForSEO authentication failed")
        return True
    return False
```

### 5.2 Insufficient Funds

```python
def handle_insufficient_funds(error: Exception):
    """Handle insufficient balance errors"""
    
    if 'insufficient funds' in str(error).lower():
        logger.error("DataForSEO account balance too low")
        await notify_human("⚠️ DataForSEO: Please add funds to continue")
        return True
    return False
```

### 5.3 Rate Limits

```python
def handle_rate_limit(error: Exception):
    """Handle API rate limits"""
    
    if 'rate limit' in str(error).lower() or '429' in str(error):
        logger.warning("DataForSEO rate limit reached")
        time.sleep(60)  # Wait 1 minute
        return True  # Retry
    return False
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_keyword_suggestions():
    client = DataForSEOClient(email='test@example.com', password='test')
    
    result = client.get_keyword_suggestions(['AI software'])
    
    assert len(result) > 0
    assert 'keyword' in result[0]
    assert 'search_volume' in result[0]
```

### 6.2 Integration Tests

```python
def test_full_research():
    client = DataForSEOClient(
        email=os.getenv('DATAFORSEO_EMAIL'),
        password=os.getenv('DATAFORSEO_PASSWORD')
    )
    
    result = client.research_keywords(['AI procurement'])
    
    assert result['success'] is True
    assert result['totalKeywords'] > 0
    assert len(result['primaryKeywords']) > 0
```

---

## 7. Cost

| Service | Cost | MVP Usage | Monthly Cost |
|---------|------|-----------|--------------|
| **Keyword Suggestions** | $0.0008/keyword | 1000 queries | ~$0.80 |
| **Keyword Difficulty** | $0.001/keyword | 500 queries | ~$0.50 |
| **Related Keywords** | $0.0008/keyword | 1000 queries | ~$0.80 |
| **Initial Deposit** | $1.00 | One-time | $1.00 (first month) |

**Total Monthly Cost:** ~$2.50 (5000+ keyword queries)

---

## 8. Best Practices

1. **Cache results** - Store keyword data in Neo4j to avoid repeat queries
2. **Batch requests** - Query multiple keywords at once (up to 1000)
3. **Use location targeting** - Set location_code for relevant market
4. **Monitor balance** - Check account balance before large queries
5. **Prioritize high-value keywords** - Focus on keywords with volume >1000

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
