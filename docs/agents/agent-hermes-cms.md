# Agent Specification: Hermes CMS Sync

**ID:** `hermes-cms-sync`  
**Role:** Payload CMS Integration  
**Vertical:** Both (ProQSmart + WeFab AI)  
**Runtime:** Python 3.11  
**Type:** Real OpenClaw Agent (future — not yet built)  

---

## 1. Purpose

Sync approved content from workspace to Payload CMS. Handles authentication, content parsing, and CMS API calls.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `exec` tool call

**Example:**
```json
{
  "command": "python",
  "args": ["/root/dev/agentic-pipeline/utilities/cms-sync/agent.py"],
  "env": {
    "FILEPATH": "/root/.openclaw-pm/workspace-seo-a/optimized/2026-07-26-ai-procurement.md",
    "VERTICAL": "A"
  }
}
```

### 2.2 From Workspace

**Files:**
- Optimized articles: `/root/.openclaw-pm/workspace-seo-*/optimized/*.md`
- JSON-LD schema: `/root/.openclaw-pm/workspace-seo-*/schema/*.jsonld`

---

## 3. Outputs

### 3.1 To Payload CMS

**API Calls:**
```python
POST /api/posts
{
  "title": "AI Procurement Software: Complete Guide",
  "slug": "ai-procurement-software-guide",
  "content": "...",
  "seo": {
    "metaTitle": "...",
    "metaDescription": "...",
    "keywords": ["AI procurement software"],
    "structuredData": {...}
  },
  "status": "draft",
  "publishedAt": "2026-07-26T10:00:00Z"
}
```

### 3.2 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-129"
    input: {
      description: """
      ✅ CMS Sync Complete
      
      **Posts Created:** 10
      - Status: All draft (ready for review)
      - SEO optimized: ✅
      - Schema included: ✅
      
      **CMS URLs:**
      - https://cms.proqsmart.com/admin/collections/posts/xxx
      - ...
      
      **Next:** Deploy to production
      """
      stateId: "done"
    }
  ) {
    success
  }
}
```

---

## 4. Implementation

### 4.1 Agent Script

```python
#!/usr/bin/env python3
"""
Real OpenClaw Agent (future): Payload CMS Content Sync
"""

import requests
import frontmatter
import json
import os
import sys
from pathlib import Path
from datetime import datetime

class CMSSyncAgent:
    def __init__(self):
        self.payload_url = os.getenv('PAYLOAD_URL', 'http://localhost:3001')
        self.email = os.getenv('PAYLOAD_EMAIL', 'admin@payload.com')
        self.password = os.getenv('PAYLOAD_PASSWORD', 'admin')
        self.token = self.login()
    
    def login(self) -> str:
        """Authenticate with Payload CMS"""
        response = requests.post(
            f'{self.payload_url}/api/users/login',
            json={'email': self.email, 'password': self.password}
        )
        
        if response.status_code == 200:
            return response.json()['token']
        else:
            raise Exception(f"Payload login failed: {response.text}")
    
    def parse_article(self, filepath: str) -> dict:
        """Parse markdown file with frontmatter"""
        with open(filepath) as f:
            post = frontmatter.load(f)
        
        return {
            'title': post.get('title', 'Untitled'),
            'slug': post.get('slug', ''),
            'content': post.content,
            'metaDescription': post.get('metaDescription', ''),
            'targetKeyword': post.get('targetKeyword', ''),
            'wordCount': post.get('wordCount', 0),
            'publishedAt': post.get('publishedAt', datetime.now().isoformat())
        }
    
    def load_schema(self, filepath: str) -> dict:
        """Load JSON-LD schema if exists"""
        schema_path = filepath.replace('.md', '.jsonld')
        
        if Path(schema_path).exists():
            with open(schema_path) as f:
                return json.load(f)
        
        return {}
    
    def sync_article(self, filepath: str, vertical: str) -> dict:
        """Sync article to Payload CMS"""
        
        article = self.parse_article(filepath)
        schema = self.load_schema(filepath)
        
        # Determine collection
        collection = 'posts'  # or 'posts-a' for multi-tenant
        
        # Prepare Payload data
        payload_data = {
            'title': article['title'],
            'slug': article['slug'],
            'content': article['content'],
            'seo': {
                'metaTitle': article['title'],
                'metaDescription': article['metaDescription'],
                'keywords': [article['targetKeyword']],
                'structuredData': schema
            },
            'status': 'draft',  # Human publishes manually
            'publishedAt': article['publishedAt']
        }
        
        # Create in Payload
        response = requests.post(
            f'{self.payload_url}/api/{collection}',
            headers={
                'Authorization': f'JWT {self.token}',
                'Content-Type': 'application/json'
            },
            json=payload_data
        )
        
        if response.status_code == 201:
            result = response.json()
            return {
                'success': True,
                'postId': result['doc']['id'],
                'slug': result['doc']['slug'],
                'cmsUrl': f"{self.payload_url}/admin/collections/{collection}/{result['doc']['id']}"
            }
        else:
            raise Exception(f"Payload API error: {response.text}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: agent.py <filepath> <vertical>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    vertical = sys.argv[2]
    
    try:
        agent = CMSSyncAgent()
        result = agent.sync_article(filepath, vertical)
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)
```

---

## 5. Configuration

### 5.1 Environment Variables

```bash
# .env
PAYLOAD_URL=http://localhost:3001
PAYLOAD_EMAIL=admin@payload.com
PAYLOAD_PASSWORD=your-secure-password
```

### 5.2 Requirements

```txt
requests==2.31.0
python-frontmatter==1.1.0
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_parse_article():
    agent = CMSSyncAgent()
    
    article = agent.parse_article('workspace-seo-a/optimized/test-article.md')
    
    assert 'title' in article
    assert 'content' in article
    assert 'slug' in article
```

### 6.2 Integration Tests

```python
def test_full_sync():
    agent = CMSSyncAgent()
    
    result = agent.sync_article(
        'workspace-seo-a/optimized/test-article.md',
        'A'
    )
    
    assert result['success'] is True
    assert result['postId'] is not None
```

---

## 7. Error Handling

### 7.1 Authentication Failures

```python
try:
    token = login()
except Exception as e:
    logger.error(f"Payload authentication failed: {e}")
    # Notify human
    await notify_human("⚠️ Payload CMS authentication failed")
    sys.exit(1)
```

### 7.2 API Failures

```python
try:
    result = sync_article(filepath, vertical)
except requests.HTTPError as e:
    logger.error(f"Payload API error: {e}")
    # Retry with exponential backoff
    time.sleep(60)
    result = sync_article(filepath, vertical)
```

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
