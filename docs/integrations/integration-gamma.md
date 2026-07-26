# Integration Specification: Gamma.app

**Service:** Gamma.app Infographic Generation  
**Purpose:** Create visual infographics from content  
**Integration Type:** REST API  
**Cost:** Free tier available  

---

## 1. Overview

Gamma.app generates infographics and visual content from text. The Designer agent uses Gamma to create shareable visuals for social media and blog posts.

---

## 2. Setup

### 2.1 Create Account

1. Visit https://gamma.app
2. Sign up for free account
3. Go to Settings → API
4. Generate API key

### 2.2 Configure Environment

```bash
# .env
GAMMA_API_KEY=xxx
GAMMA_BASE_URL=https://public-api.gamma.app/v1
```

---

## 3. API Endpoints

### 3.1 Generate Infographic

```http
POST /generations
Content-Type: application/json
X-API-KEY: {api_key}

{
  "type": "infographic",
  "content": "AI procurement software reduces costs by 30%",
  "style": "professional",
  "format": "png"
}
```

**Response:**
```json
{
  "id": "gen_xxx",
  "status": "completed",
  "url": "https://gamma.app/api/files/infographic_xxx.png",
  "thumbnail": "https://gamma.app/api/files/thumb_xxx.png"
}
```

### 3.2 Get Generation Status

```http
GET /generations/{id}
X-API-KEY: {api_key}
```

**Response:**
```json
{
  "id": "gen_xxx",
  "status": "processing",
  "progress": 75
}
```

### 3.3 List Templates

```http
GET /templates
X-API-KEY: {api_key}
```

**Response:**
```json
{
  "templates": [
    {
      "id": "tpl_xxx",
      "name": "Professional Infographic",
      "category": "business"
    }
  ]
}
```

---

## 4. Python Client

### 4.1 Gamma Client Class

```python
#!/usr/bin/env python3
"""
Gamma.app API Client
Generates infographics from text content
"""

import requests
import time
from typing import Dict, Optional

class GammaClient:
    def __init__(self, api_key: str):
        self.base_url = 'https://public-api.gamma.app/v1'
        self.headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    
    def generate_infographic(self, content: str, style: str = 'professional') -> Dict:
        """Generate infographic from text"""
        
        payload = {
            'type': 'infographic',
            'content': content,
            'style': style,
            'format': 'png'
        }
        
        response = requests.post(
            f'{self.base_url}/generations',
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Gamma API error: {response.text}")
    
    def get_status(self, generation_id: str) -> Dict:
        """Get generation status"""
        
        response = requests.get(
            f'{self.base_url}/generations/{generation_id}',
            headers=self.headers,
            timeout=30
        )
        
        return response.json()
    
    def wait_for_completion(self, generation_id: str, timeout_seconds: int = 120) -> Dict:
        """Wait for generation to complete"""
        
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            status = self.get_status(generation_id)
            
            if status['status'] == 'completed':
                return status
            elif status['status'] == 'failed':
                raise Exception(f"Generation failed: {status.get('error', 'Unknown error')}")
            
            time.sleep(5)  # Poll every 5 seconds
        
        raise Exception("Generation timed out")
    
    def download(self, url: str, filepath: str):
        """Download generated infographic"""
        
        response = requests.get(url, timeout=60)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
    
    def create_infographic(self, content: str, output_path: str, style: str = 'professional') -> Dict:
        """Full workflow: generate, wait, download"""
        
        # Step 1: Generate
        print(f"🎨 Generating infographic...")
        result = self.generate_infographic(content, style)
        generation_id = result['id']
        
        # Step 2: Wait
        print(f"⏳ Waiting for completion...")
        result = self.wait_for_completion(generation_id)
        
        # Step 3: Download
        print(f"📥 Downloading infographic...")
        self.download(result['url'], output_path)
        
        return {
            'success': True,
            'generationId': generation_id,
            'filepath': output_path,
            'url': result['url']
        }

# Usage
if __name__ == '__main__':
    import os
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: gamma.py <content> <output_path>")
        sys.exit(1)
    
    content = sys.argv[1]
    output_path = sys.argv[2]
    
    client = GammaClient(api_key=os.getenv('GAMMA_API_KEY'))
    result = client.create_infographic(content, output_path)
    
    print(f"✅ Infographic created: {result['filepath']}")
```

---

## 5. Error Handling

### 5.1 Rate Limits

```python
def handle_rate_limit(error: Exception):
    """Handle Gamma API rate limits"""
    
    if 'rate limit' in str(error).lower():
        logger.warning("Gamma API rate limit reached")
        time.sleep(60)  # Wait 1 minute
        return True  # Retry
    return False
```

### 5.2 Generation Failures

```python
def handle_generation_failure(generation_id: str):
    """Handle failed generation"""
    
    status = client.get_status(generation_id)
    error = status.get('error', 'Unknown error')
    
    logger.error(f"Gamma generation failed: {error}")
    
    # Notify human
    await notify_human(f"⚠️ Infographic generation failed: {error}")
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_generate_infographic():
    client = GammaClient(api_key='test_key')
    
    result = client.generate_infographic(
        "AI reduces costs by 30%",
        style='professional'
    )
    
    assert 'id' in result
    assert result['status'] in ['processing', 'completed']
```

### 6.2 Integration Tests

```python
def test_full_workflow():
    client = GammaClient(api_key=os.getenv('GAMMA_API_KEY'))
    
    result = client.create_infographic(
        "Test content",
        "/tmp/test-infographic.png"
    )
    
    assert result['success'] is True
    assert Path(result['filepath']).exists()
```

---

## 7. Cost

| Tier | Price | Generations/Month | MVP Usage |
|------|-------|-------------------|-----------|
| **Free** | $0 | 10 | 5-10/month (sufficient) |
| **Plus** | $10/mo | 100 | Not needed for MVP |
| **Pro** | $20/mo | Unlimited | Future scaling |

**MVP Cost:** $0 (Free tier sufficient)

---

## 8. Best Practices

1. **Keep content concise** - Gamma works best with 1-2 sentence inputs
2. **Specify style** - Use 'professional', 'modern', or 'minimal'
3. **Poll efficiently** - Check status every 5 seconds, not faster
4. **Cache results** - Don't regenerate same infographic
5. **Use templates** - List templates first for consistent branding

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
