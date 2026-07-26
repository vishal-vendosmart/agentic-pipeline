# Integration Specification: Payload CMS

**Service:** Payload CMS  
**Purpose:** Content management, blog posts, landing pages  
**Integration Type:** REST API + Webhooks  
**Cost:** Self-hosted (free, open-source)  

---

## 1. Overview

Payload CMS stores all published content including blog posts, landing pages, and site configuration. The Hermes CMS agent syncs optimized content from the workspace to Payload collections.

---

## 2. Setup

### 2.1 Docker Installation

```bash
docker run -d \
  --name payload \
  -p 3001:3000 \
  -v payload-data:/app/payload \
  -e PAYLOAD_SECRET=your-secret-key \
  -e MONGODB_URI=mongodb://payload-mongo:27017/payload \
  ghcr.io/payloadcms/payload:latest
```

### 2.2 Access

- **Admin UI:** http://localhost:3001/admin
- **API:** http://localhost:3001/api
- **Default admin:** admin@payload.com / admin

---

## 3. Collections

### 3.1 Posts Collection

```typescript
// payload.config.ts
const Posts = {
  slug: 'posts',
  labels: {
    singular: 'Post',
    plural: 'Posts'
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      required: true
    },
    {
      name: 'slug',
      type: 'text',
      required: true,
      unique: true
    },
    {
      name: 'content',
      type: 'richText',
      required: true
    },
    {
      name: 'seo',
      type: 'group',
      fields: [
        {
          name: 'metaTitle',
          type: 'text',
          required: true
        },
        {
          name: 'metaDescription',
          type: 'text',
          required: true
        },
        {
          name: 'keywords',
          type: 'array',
          of: [{ type: 'text' }]
        },
        {
          name: 'structuredData',
          type: 'json'
        }
      ]
    },
    {
      name: 'status',
      type: 'select',
      options: ['draft', 'published'],
      defaultValue: 'draft'
    },
    {
      name: 'publishedAt',
      type: 'date'
    }
  ],
  versions: {
    drafts: true
  }
};
```

### 3.2 Pages Collection

```typescript
const Pages = {
  slug: 'pages',
  fields: [
    {
      name: 'title',
      type: 'text',
      required: true
    },
    {
      name: 'slug',
      type: 'text',
      required: true,
      unique: true
    },
    {
      name: 'pageType',
      type: 'select',
      options: ['landing', 'blog', 'about', 'contact'],
      required: true
    },
    {
      name: 'content',
      type: 'richText'
    },
    {
      name: 'components',
      type: 'json',
      description: 'React component structure'
    }
  ]
};
```

---

## 4. API Integration

### 4.1 Authentication

```python
import requests

class PayloadClient:
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url
        self.token = self.login(email, password)
    
    def login(self, email: str, password: str) -> str:
        response = requests.post(
            f'{self.base_url}/api/users/login',
            json={'email': email, 'password': password}
        )
        
        if response.status_code == 200:
            return response.json()['token']
        else:
            raise Exception(f"Payload login failed: {response.text}")
    
    def create_post(self, post_data: dict) -> dict:
        response = requests.post(
            f'{self.base_url}/api/posts',
            headers={
                'Authorization': f'JWT {self.token}',
                'Content-Type': 'application/json'
            },
            json=post_data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Payload API error: {response.text}")
    
    def update_post(self, post_id: str, updates: dict) -> dict:
        response = requests.patch(
            f'{self.base_url}/api/posts/{post_id}',
            headers={
                'Authorization': f'JWT {self.token}',
                'Content-Type': 'application/json'
            },
            json=updates
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Payload API error: {response.text}")
```

### 4.2 Usage Example

```python
# Initialize client
client = PayloadClient(
    base_url='http://localhost:3001',
    email='admin@payload.com',
    password='admin'
)

# Create post
post_data = {
    'title': 'AI Procurement Software: Complete Guide',
    'slug': 'ai-procurement-software-guide',
    'content': '...',
    'seo': {
        'metaTitle': 'AI Procurement Software Guide | ProQSmart',
        'metaDescription': 'Complete guide...',
        'keywords': ['AI procurement', 'manufacturing'],
        'structuredData': {...}
    },
    'status': 'draft'
}

result = client.create_post(post_data)
print(f"Created post: {result['doc']['id']}")
```

---

## 5. Webhooks

### 5.1 Setup Webhook

1. Go to Admin → Settings → Webhooks
2. Click "Create new webhook"
3. URL: `https://your-domain.com/api/webhooks/payload`
4. Trigger: `posts.create`, `posts.update`
5. Save

### 5.2 Webhook Handler

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/webhooks/payload', methods=['POST'])
def handle_payload_webhook():
    data = request.json
    
    if data['collection'] == 'posts':
        if data['action'] == 'afterChange':
            post_id = data['doc']['id']
            status = data['doc']['status']
            
            if status == 'published':
                on_post_published(post_id)
            elif status == 'draft':
                on_post_saved_as_draft(post_id)
    
    return 'OK', 200
```

---

## 6. Hermes CMS Agent

### 6.1 Sync Script

```python
#!/usr/bin/env python3
"""
Hermes Agent: Payload CMS Content Sync
Syncs approved content from workspace to Payload CMS
"""

import requests
import frontmatter
import json
import sys
from pathlib import Path

class CMSSyncAgent:
    def __init__(self, payload_url: str, email: str, password: str):
        self.client = PayloadClient(payload_url, email, password)
    
    def sync_article(self, filepath: str, vertical: str) -> dict:
        """Sync article to Payload CMS"""
        
        # Parse markdown
        with open(filepath) as f:
            post = frontmatter.load(f)
        
        # Prepare Payload data
        collection = 'posts'  # or 'posts-a' for multi-tenant
        payload_data = {
            'title': post.get('title', 'Untitled'),
            'slug': post.get('slug', ''),
            'content': post.content,
            'seo': {
                'metaTitle': post.get('metaTitle', ''),
                'metaDescription': post.get('metaDescription', ''),
                'keywords': [post.get('targetKeyword', '')],
                'structuredData': self.load_schema(filepath)
            },
            'status': 'draft',  # Human publishes manually
            'publishedAt': post.get('publishedAt')
        }
        
        # Create in Payload
        result = self.client.create_post(payload_data)
        
        return {
            'success': True,
            'postId': result['doc']['id'],
            'slug': result['doc']['slug'],
            'cmsUrl': f"{payload_url}/admin/collections/{collection}/{result['doc']['id']}"
        }
    
    def load_schema(self, filepath: str) -> dict:
        """Load JSON-LD schema if exists"""
        schema_path = filepath.replace('.md', '.jsonld')
        
        if Path(schema_path).exists():
            with open(schema_path) as f:
                return json.load(f)
        
        return {}

# Usage
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: agent.py <filepath> <vertical>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    vertical = sys.argv[2]
    
    agent = CMSSyncAgent(
        payload_url='http://localhost:3001',
        email='admin@payload.com',
        password='admin'
    )
    
    result = agent.sync_article(filepath, vertical)
    print(json.dumps(result, indent=2))
```

---

## 7. Testing

### 7.1 Unit Tests

```python
def test_create_post():
    client = PayloadClient('http://localhost:3001', 'admin', 'admin')
    
    post_data = {
        'title': 'Test Post',
        'slug': 'test-post',
        'content': 'Test content',
        'status': 'draft'
    }
    
    result = client.create_post(post_data)
    
    assert result['doc']['id'] is not None
    assert result['doc']['slug'] == 'test-post'
```

### 7.2 Integration Tests

```python
def test_full_sync():
    agent = CMSSyncAgent('http://localhost:3001', 'admin', 'admin')
    
    result = agent.sync_article(
        'workspace-vertical-a/drafts/test-article.md',
        'A'
    )
    
    assert result['success'] is True
    assert result['postId'] is not None
```

---

## 8. Cost

| Component | Cost | Notes |
|-----------|------|-------|
| **Payload CMS** | $0 | Open-source, self-hosted |
| **MongoDB** | $0 | Self-hosted (Docker) |
| **Docker** | $0 | Included |
| **Storage** | $0 | Included |

**Total Monthly Cost:** $0

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
