# Integration Specification: SerpAPI

**Service:** SerpAPI  
**Purpose:** SERP analysis, competitor research, ranking tracking  
**Integration Type:** REST API  
**Cost:** Free tier (100 searches/month)  

---

## 1. Overview

SerpAPI provides real-time search engine results pages (SERP) data. The Researcher agent uses SerpAPI to analyze competitor content, discover content gaps, and track keyword rankings.

---

## 2. Setup

### 2.1 Create Account

1. Visit https://serpapi.com
2. Sign up for free account
3. Copy API key from dashboard
4. Note rate limit: 100 searches/month (free tier)

### 2.2 Configure Environment

```bash
# .env
SERPAPI_KEY=your-api-key
SERPAPI_BASE_URL=https://serpapi.com/search
```

### 2.3 Install Dependencies

```bash
pip install google-search-results
```

---

## 3. API Endpoints

### 3.1 Google Search Results

```http
GET /search?q={query}&api_key={key}&engine=google
```

**Example:**
```
GET /search?q=AI+procurement+software&api_key=xxx&engine=google&num=10
```

**Response:**
```json
{
  "search_metadata": {
    "id": "search_xxx",
    "status": "Success",
    "created_at": "2026-07-26T10:00:00Z",
    "processed_at": "2026-07-26T10:00:01Z",
    "total_time_taken": 1.2
  },
  "search_parameters": {
    "engine": "google",
    "q": "AI procurement software",
    "google_domain": "google.com",
    "num": 10
  },
  "organic_results": [
    {
      "position": 1,
      "title": "Best AI Procurement Software 2026",
      "link": "https://competitor.com/ai-procurement",
      "displayed_link": "competitor.com",
      "snippet": "Compare top AI procurement solutions...",
      "snippet_highlighted_words": ["AI", "procurement"]
    }
  ],
  "related_searches": [
    {
      "query": "AI procurement tools",
      "link": "https://google.com/search?q=AI+procurement+tools"
    }
  ]
}
```

### 3.2 Google Shopping Results

```http
GET /search?q={query}&api_key={key}&engine=google_shopping
```

### 3.3 Google News Results

```http
GET /search?q={query}&api_key={key}&engine=google_news
```

---

## 4. Python Client

### 4.1 SerpAPI Client Class

```python
#!/usr/bin/env python3
"""
SerpAPI Client
SERP analysis and competitor research
"""

import requests
from typing import Dict, List

class SerpAPIClient:
    def __init__(self, api_key: str):
        self.base_url = 'https://serpapi.com/search'
        self.params = {
            'api_key': api_key,
            'engine': 'google',
            'google_domain': 'google.com',
            'hl': 'en',
            'gl': 'us'
        }
    
    def search(self, query: str, num_results: int = 10) -> Dict:
        """Get Google search results"""
        
        params = {
            **self.params,
            'q': query,
            'num': num_results
        }
        
        response = requests.get(self.base_url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"SerpAPI error: {response.text}")
    
    def get_organic_results(self, query: str, num_results: int = 10) -> List[Dict]:
        """Get organic search results only"""
        
        results = self.search(query, num_results)
        return results.get('organic_results', [])
    
    def analyze_competitors(self, query: str) -> Dict:
        """Analyze competitor content for a keyword"""
        
        print(f"🔍 Analyzing competitors for: {query}")
        
        results = self.get_organic_results(query, num_results=10)
        
        competitors = []
        for result in results:
            competitors.append({
                'position': result.get('position'),
                'title': result.get('title'),
                'url': result.get('link'),
                'domain': result.get('displayed_link'),
                'snippet': result.get('snippet'),
                'wordCount': len(result.get('snippet', '').split())
            })
        
        # Analyze
        avg_word_count = sum(c['wordCount'] for c in competitors) / len(competitors)
        domains = [c['domain'] for c in competitors]
        
        return {
            'success': True,
            'query': query,
            'totalResults': len(competitors),
            'competitors': competitors,
            'averageWordCount': round(avg_word_count, 0),
            'topDomains': domains[:5]
        }
    
    def get_related_searches(self, query: str) -> List[str]:
        """Get related search queries"""
        
        results = self.search(query)
        related = results.get('related_searches', [])
        
        return [r['query'] for r in related]
    
    def track_ranking(self, keyword: str, domain: str) -> Dict:
        """Track ranking for a specific domain and keyword"""
        
        results = self.get_organic_results(keyword, num_results=100)
        
        for i, result in enumerate(results, 1):
            if domain in result.get('link', ''):
                return {
                    'success': True,
                    'keyword': keyword,
                    'domain': domain,
                    'position': i,
                    'url': result.get('link')
                }
        
        return {
            'success': True,
            'keyword': keyword,
            'domain': domain,
            'position': None,  # Not in top 100
            'message': 'Not found in top 100'
        }

# Usage
if __name__ == '__main__':
    import os
    import json
    
    client = SerpAPIClient(api_key=os.getenv('SERPAPI_KEY'))
    
    # Analyze competitors
    result = client.analyze_competitors('AI procurement software')
    print(json.dumps(result, indent=2))
    
    # Track ranking
    ranking = client.track_ranking(
        'AI procurement software',
        'proqsmart.com'
    )
    print(f"Ranking: {ranking['position']}")
```

---

## 5. Error Handling

### 5.1 Rate Limit Errors

```python
def handle_rate_limit(error: Exception):
    """Handle SerpAPI rate limit errors"""
    
    if 'rate limit' in str(error).lower() or '429' in str(error):
        logger.warning("SerpAPI rate limit reached (100 searches/month)")
        await notify_human("⚠️ SerpAPI: Free tier limit reached")
        return True
    return False
```

### 5.2 Invalid Query

```python
def handle_invalid_query(error: Exception, query: str):
    """Handle invalid or blocked queries"""
    
    if '400' in str(error) or 'bad request' in str(error).lower():
        logger.error(f"Invalid SerpAPI query: {query}")
        return True
    return False
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_search():
    client = SerpAPIClient(api_key='test_key')
    
    # Mock response for testing
    results = client.get_organic_results('test query')
    
    assert isinstance(results, list)
```

### 6.2 Integration Tests

```python
def test_competitor_analysis():
    client = SerpAPIClient(api_key=os.getenv('SERPAPI_KEY'))
    
    result = client.analyze_competitors('AI software')
    
    assert result['success'] is True
    assert result['totalResults'] > 0
    assert result['averageWordCount'] > 0
```

---

## 7. Cost

| Tier | Price | Searches/Month | MVP Usage |
|------|-------|----------------|-----------|
| **Free** | $0 | 100 | 50-80/month (sufficient) |
| **Lite** | $75/mo | 5000 | Not needed for MVP |
| **Standard** | $150/mo | 15000 | Future scaling |

**MVP Cost:** $0 (Free tier sufficient)

---

## 8. Best Practices

1. **Cache results** - Store SERP data to avoid repeat queries
2. **Use wisely** - Free tier only has 100 searches/month
3. **Focus on high-value keywords** - Prioritize primary keywords
4. **Track over time** - Run same queries monthly to track changes
5. **Analyze snippets** - Use snippet data to understand content angles

---

## 9. Example: Content Gap Analysis

```python
def analyze_content_gap(keyword: str):
    """Identify content gaps from SERP analysis"""
    
    client = SerpAPIClient(api_key=os.getenv('SERPAPI_KEY'))
    
    # Get top 10 results
    results = client.get_organic_results(keyword, num_results=10)
    
    # Analyze content types
    content_types = []
    for result in results:
        title = result.get('title', '').lower()
        if 'guide' in title:
            content_types.append('guide')
        elif 'vs' in title or 'comparison' in title:
            content_types.append('comparison')
        elif 'best' in title:
            content_types.append('listicle')
        elif 'how to' in title:
            content_types.append('tutorial')
    
    # Identify gaps
    all_types = ['guide', 'comparison', 'listicle', 'tutorial', 'case_study', 'roi_calculator']
    gaps = [t for t in all_types if t not in content_types]
    
    return {
        'keyword': keyword,
        'existingContent': content_types,
        'gaps': gaps,
        'opportunity': f"Create {gaps[0]} content for {keyword}" if gaps else "Market saturated"
    }

# Usage
gap_analysis = analyze_content_gap('AI procurement software')
print(gap_analysis)
# Output: {'gaps': ['case_study', 'roi_calculator'], 'opportunity': 'Create case_study content'}
```

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
