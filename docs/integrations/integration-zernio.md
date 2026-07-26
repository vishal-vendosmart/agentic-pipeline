# Integration Specification: Zernio

**Service:** Zernio Social Media Scheduling  
**Purpose:** Auto-post content to social platforms  
**Integration Type:** REST API  
**Cost:** Free tier available  

---

## 1. Overview

Zernio automates social media posting across platforms (Twitter, LinkedIn, Facebook). The Writer agent uses Zernio to schedule promotional posts for published content.

---

## 2. Setup

### 2.1 Create Account

1. Visit https://zernio.com
2. Sign up for free account
3. Connect social accounts (Twitter, LinkedIn, Facebook)
4. Go to Settings → API
5. Generate API key

### 2.2 Configure Environment

```bash
# .env
ZERNIO_API_KEY=sk_xxx  # Replace with actual key in .env
ZERNIO_BASE_URL=https://zernio.com/api/v1
```

---

## 3. API Endpoints

### 3.1 Create Post

```http
POST /posts
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "content": "New blog post: AI Procurement Software Guide",
  "url": "https://proqsmart.com/blog/ai-procurement-software-guide",
  "platforms": ["twitter", "linkedin"],
  "scheduleAt": "2026-07-26T14:00:00Z"
}
```

**Response:**
```json
{
  "id": "post_xxx",
  "status": "scheduled",
  "platforms": {
    "twitter": { "id": "tw_xxx", "status": "scheduled" },
    "linkedin": { "id": "li_xxx", "status": "scheduled" }
  }
}
```

### 3.2 Get Post Status

```http
GET /posts/{id}
Authorization: Bearer {api_key}
```

**Response:**
```json
{
  "id": "post_xxx",
  "status": "published",
  "publishedAt": "2026-07-26T14:00:00Z",
  "analytics": {
    "twitter": { "likes": 15, "retweets": 5 },
    "linkedin": { "likes": 23, "shares": 8 }
  }
}
```

### 3.3 Schedule Bulk Posts

```http
POST /posts/bulk
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "posts": [
    {
      "content": "Post 1",
      "scheduleAt": "2026-07-26T14:00:00Z"
    },
    {
      "content": "Post 2",
      "scheduleAt": "2026-07-27T14:00:00Z"
    }
  ]
}
```

---

## 4. Python Client

### 4.1 Zernio Client Class

```python
#!/usr/bin/env python3
"""
Zernio API Client
Schedules and posts to social media platforms
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List

class ZernioClient:
    def __init__(self, api_key: str):
        self.base_url = 'https://zernio.com/api/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_post(self, content: str, url: str = None, 
                    platforms: List[str] = None, 
                    schedule_at: datetime = None) -> Dict:
        """Create a social media post"""
        
        if platforms is None:
            platforms = ['twitter', 'linkedin']
        
        payload = {
            'content': content,
            'platforms': platforms
        }
        
        if url:
            payload['url'] = url
        
        if schedule_at:
            payload['scheduleAt'] = schedule_at.isoformat() + 'Z'
        
        response = requests.post(
            f'{self.base_url}/posts',
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Zernio API error: {response.text}")
    
    def get_post(self, post_id: str) -> Dict:
        """Get post details"""
        
        response = requests.get(
            f'{self.base_url}/posts/{post_id}',
            headers=self.headers,
            timeout=30
        )
        
        return response.json()
    
    def schedule_bulk(self, posts: List[Dict]) -> Dict:
        """Schedule multiple posts"""
        
        response = requests.post(
            f'{self.base_url}/posts/bulk',
            headers=self.headers,
            json={'posts': posts},
            timeout=60
        )
        
        return response.json()
    
    def schedule_promotion(self, article_url: str, article_title: str) -> Dict:
        """Schedule promotional posts for an article"""
        
        # Create multiple posts over time
        posts = [
            {
                'content': f"New blog post: {article_title}",
                'url': article_url,
                'scheduleAt': (datetime.now() + timedelta(hours=1)).isoformat() + 'Z'
            },
            {
                'content': f"Learn about {article_title} - insights for manufacturing SMEs",
                'url': article_url,
                'scheduleAt': (datetime.now() + timedelta(days=1)).isoformat() + 'Z'
            },
            {
                'content': f"Must read: {article_title} #AI #Manufacturing",
                'url': article_url,
                'scheduleAt': (datetime.now() + timedelta(days=3)).isoformat() + 'Z'
            }
        ]
        
        return self.schedule_bulk(posts)

# Usage
if __name__ == '__main__':
    import os
    
    client = ZernioClient(api_key=os.getenv('ZERNIO_API_KEY'))
    
    # Schedule promotion for new article
    result = client.schedule_promotion(
        article_url='https://proqsmart.com/blog/ai-procurement-guide',
        article_title='AI Procurement Software: Complete Guide'
    )
    
    print(f"✅ Scheduled {len(result['posts'])} posts")
```

---

## 5. Error Handling

### 5.1 Authentication Errors

```python
def handle_auth_error(error: Exception):
    """Handle Zernio authentication failures"""
    
    if '401' in str(error) or 'unauthorized' in str(error).lower():
        logger.error("Zernio API key invalid")
        await notify_human("⚠️ Zernio authentication failed")
        return True
    return False
```

### 5.2 Platform Errors

```python
def handle_platform_error(post_id: str, platform: str):
    """Handle individual platform posting errors"""
    
    post = client.get_post(post_id)
    platform_status = post['platforms'].get(platform, {})
    
    if platform_status.get('status') == 'failed':
        error = platform_status.get('error', 'Unknown error')
        logger.error(f"{platform} post failed: {error}")
        
        # Retry with different content
        if 'character limit' in error.lower():
            logger.info("Retrying with shorter content")
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_create_post():
    client = ZernioClient(api_key='test_key')
    
    result = client.create_post(
        content="Test post",
        platforms=['twitter']
    )
    
    assert 'id' in result
    assert result['status'] in ['scheduled', 'published']
```

### 6.2 Integration Tests

```python
def test_schedule_promotion():
    client = ZernioClient(api_key=os.getenv('ZERNIO_API_KEY'))
    
    result = client.schedule_promotion(
        article_url='https://example.com/test',
        article_title='Test Article'
    )
    
    assert len(result['posts']) == 3
    for post in result['posts']:
        assert 'id' in post
```

---

## 7. Cost

| Tier | Price | Posts/Month | MVP Usage |
|------|-------|-------------|-----------|
| **Free** | $0 | 30 | 20-30/month (sufficient) |
| **Pro** | $15/mo | 200 | Not needed for MVP |
| **Business** | $50/mo | Unlimited | Future scaling |

**MVP Cost:** $0 (Free tier sufficient)

---

## 8. Best Practices

1. **Space out posts** - Don't post same content multiple times in one day
2. **Vary messaging** - Use different angles for each platform
3. **Include visuals** - Posts with images get 2x engagement
4. **Monitor analytics** - Track which posts perform best
5. **Respect rate limits** - Free tier: 30 posts/month

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
