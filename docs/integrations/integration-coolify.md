# Integration Specification: Coolify

**Service:** Coolify Deployment Automation  
**Purpose:** Deploy content to production  
**Integration Type:** Webhooks + REST API  
**Cost:** Self-hosted (free, open-source)  

---

## 1. Overview

Coolify automates deployment of optimized content to production. The Hermes Deploy agent triggers Coolify webhooks to deploy sites after content approval.

---

## 2. Setup

### 2.1 Installation

Follow Coolify installation guide at https://coolify.io/docs/installation

**Recommended:** Install on Hetzner VPS (same server as other services)

### 2.2 Access

- **Dashboard:** http://localhost:8000
- **API:** http://localhost:8000/api
- **Default:** admin / password (change immediately!)

---

## 3. Webhooks

### 3.1 Create Webhook

1. Go to Project → Your Project → Deployments
2. Click "Add webhook"
3. Configure:
   - **Name:** "Content Deployment"
   - **Branch:** main
   - **Environment:** production
4. Copy webhook URL

### 3.2 Webhook URL Format

```
http://localhost:8000/api/webhooks/deploy/{project-id}/{environment-id}
```

---

## 4. Hermes Deploy Agent

### 4.1 Deploy Script

```python
#!/usr/bin/env python3
"""
Real OpenClaw Agent (future): Coolify Deployment Trigger
Triggers deployment via Coolify webhooks and verifies success
"""

import requests
import json
import sys
import time
from typing import Dict

class DeployAgent:
    def __init__(self, coolify_url: str, webhook_url: str):
        self.coolify_url = coolify_url
        self.webhook_url = webhook_url
    
    def trigger_deployment(self, site: str) -> Dict:
        """Trigger Coolify deployment"""
        
        response = requests.post(
            self.webhook_url,
            json={
                'site': site,
                'environment': 'production',
                'branch': 'main'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Coolify webhook failed: {response.text}")
    
    def wait_for_deployment(self, deployment_id: str, timeout_seconds: int = 300) -> bool:
        """Poll Coolify API until deployment completes"""
        
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            response = requests.get(
                f'{self.coolify_url}/api/deployments/{deployment_id}',
                timeout=30
            )
            
            status = response.json().get('status')
            
            if status == 'ready':
                return True
            elif status in ['failed', 'cancelled']:
                return False
            
            time.sleep(10)  # Poll every 10 seconds
        
        return False  # Timeout
    
    def verify_site_health(self, domain: str) -> bool:
        """Verify deployed site is accessible"""
        
        try:
            response = requests.get(
                f'https://{domain}',
                timeout=30,
                headers={'User-Agent': 'Coolify-Deploy-Agent'}
            )
            return response.status_code == 200
        except:
            return False
    
    def deploy(self, vertical: str, domain: str) -> Dict:
        """Full deployment workflow"""
        
        # Step 1: Trigger deployment
        print(f"Triggering deployment for {vertical}...")
        deployment = self.trigger_deployment(vertical)
        
        # Step 2: Wait for completion
        print(f"Waiting for deployment {deployment['id']}...")
        success = self.wait_for_deployment(deployment['id'])
        
        if not success:
            return {
                'success': False,
                'error': 'Deployment failed or timed out',
                'deploymentId': deployment['id']
            }
        
        # Step 3: Verify site health
        print(f"Verifying site health at {domain}...")
        healthy = self.verify_site_health(domain)
        
        if not healthy:
            return {
                'success': False,
                'error': 'Site health check failed',
                'deploymentId': deployment['id']
            }
        
        return {
            'success': True,
            'deploymentId': deployment['id'],
            'url': f"https://{domain}",
            'message': 'Deployment successful'
        }

# Usage
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: agent.py <vertical> <domain>")
        sys.exit(1)
    
    vertical = sys.argv[1]
    domain = sys.argv[2]
    
    agent = DeployAgent(
        coolify_url='http://localhost:8000',
        webhook_url='http://localhost:8000/api/webhooks/deploy/project-id/env-id'
    )
    
    result = agent.deploy(vertical, domain)
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result['success'] else 1)
```

---

## 5. Deployment Flow

### 5.1 Sequence

```
1. Hermes Deploy → Coolify Webhook
2. Coolify → Git pull (main branch)
3. Coolify → Build (npm run build)
4. Coolify → Deploy to production
5. Coolify → Health check
6. Hermes Deploy → Verify site
7. Hermes Deploy → Update Linear task
```

### 5.2 Example Response

```json
{
  "success": true,
  "deploymentId": "dep_123456",
  "url": "https://proqsmart.com",
  "message": "Deployment successful",
  "timestamp": "2026-07-26T10:00:00Z"
}
```

---

## 6. Error Handling

### 6.1 Deployment Failures

```python
def handle_deployment_failure(deployment_id: str):
    """Handle deployment failure"""
    
    # Get deployment logs
    logs = requests.get(f'{COOLIFY_URL}/api/deployments/{deployment_id}/logs')
    
    # Analyze failure
    if 'build failed' in logs.text:
        logger.error(f"Build failed: {logs.text}")
        # Notify developer
    elif 'health check failed' in logs.text:
        logger.error(f"Health check failed: {logs.text}")
        # Rollback
    else:
        logger.error(f"Unknown deployment failure: {logs.text}")
```

### 6.2 Rollback

```python
def rollback_deployment(project_id: str, previous_version: str):
    """Rollback to previous version"""
    
    response = requests.post(
        f'{COOLIFY_URL}/api/projects/{project_id}/rollback',
        json={'version': previous_version}
    )
    
    if response.status_code == 200:
        logger.info(f"Rolled back to {previous_version}")
    else:
        logger.error(f"Rollback failed: {response.text}")
```

---

## 7. Testing

### 7.1 Unit Tests

```python
def test_trigger_deployment():
    agent = DeployAgent('http://localhost:8000', 'http://localhost:8000/api/webhooks/test')
    
    result = agent.trigger_deployment('test-site')
    
    assert 'id' in result
    assert result['status'] in ['queued', 'building', 'ready']
```

### 7.2 Integration Tests

```python
def test_full_deployment():
    agent = DeployAgent('http://localhost:8000', 'http://localhost:8000/api/webhooks/test')
    
    result = agent.deploy('test-vertical', 'test.example.com')
    
    assert result['success'] is True
    assert result['deploymentId'] is not None
    assert result['url'] == 'https://test.example.com'
```

---

## 8. Cost

| Component | Cost | Notes |
|-----------|------|-------|
| **Coolify** | $0 | Open-source, self-hosted |
| **Docker** | $0 | Included |
| **Storage** | $0 | Included |

**Total Monthly Cost:** $0

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
