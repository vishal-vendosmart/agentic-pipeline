# Agent Specification: Hermes Deploy

**ID:** `hermes-deploy`  
**Role:** Coolify Deployment Automation  
**Vertical:** Both (ProQSmart + WeFab AI)  
**Runtime:** Python 3.11  
**Type:** Hermes Agent (Python script)  

---

## 1. Purpose

Deploy approved content from Payload CMS to production via Coolify. Triggers webhooks, monitors deployment, and verifies site health.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `exec` tool call

**Example:**
```json
{
  "command": "python",
  "args": ["/root/.openclaw/hermes-agents/deploy/agent.py"],
  "env": {
    "VERTICAL": "A",
    "DOMAIN": "proqsmart.com"
  }
}
```

### 2.2 Prerequisites

- Content synced to Payload CMS (draft status)
- Human approval received
- Git repository ready (main branch)

---

## 3. Outputs

### 3.1 To Coolify

**Webhook Call:**
```python
POST http://localhost:8000/api/webhooks/deploy/{project-id}/{environment-id}
{
  "site": "proqsmart.com",
  "environment": "production",
  "branch": "main"
}
```

### 3.2 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-130"
    input: {
      description: """
      ✅ Deployment Complete
      
      **Site:** proqsmart.com
      **Status:** Live
      **Deployment ID:** dep_123456
      
      **Health Check:** ✅ Passed
      **SSL:** ✅ Valid
      **Response Time:** 245ms
      
      **URL:** https://proqsmart.com
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
Hermes Agent: Coolify Deployment Trigger
"""

import requests
import json
import os
import sys
import time
from datetime import datetime

class DeployAgent:
    def __init__(self):
        self.coolify_url = os.getenv('COOLIFY_URL', 'http://localhost:8000')
        self.webhook_url = os.getenv('COOLIFY_WEBHOOK_URL')
        self.vertical = os.getenv('VERTICAL', 'A')
        self.domain = os.getenv('DOMAIN')
    
    def trigger_deployment(self) -> dict:
        """Trigger Coolify deployment via webhook"""
        
        response = requests.post(
            self.webhook_url,
            json={
                'site': self.domain,
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
    
    def verify_site_health(self) -> dict:
        """Verify deployed site is accessible and healthy"""
        
        try:
            start_time = time.time()
            
            response = requests.get(
                f'https://{self.domain}',
                timeout=30,
                headers={'User-Agent': 'Coolify-Deploy-Agent'},
                allow_redirects=True
            )
            
            response_time = (time.time() - start_time) * 1000  # ms
            
            return {
                'healthy': response.status_code == 200,
                'statusCode': response.status_code,
                'responseTime': round(response_time, 2),
                'ssl': response.url.startswith('https://')
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def deploy(self) -> dict:
        """Full deployment workflow"""
        
        print(f"🚀 Starting deployment for {self.vertical} ({self.domain})...")
        
        # Step 1: Trigger deployment
        print("📡 Triggering Coolify deployment...")
        deployment = self.trigger_deployment()
        deployment_id = deployment.get('id')
        
        if not deployment_id:
            return {
                'success': False,
                'error': 'No deployment ID returned',
                'raw': deployment
            }
        
        print(f"✅ Deployment triggered: {deployment_id}")
        
        # Step 2: Wait for completion
        print(f"⏳ Waiting for deployment to complete...")
        success = self.wait_for_deployment(deployment_id)
        
        if not success:
            return {
                'success': False,
                'error': 'Deployment failed or timed out',
                'deploymentId': deployment_id
            }
        
        print(f"✅ Deployment completed")
        
        # Step 3: Verify site health
        print(f"🏥 Verifying site health...")
        health = self.verify_site_health()
        
        if not health['healthy']:
            return {
                'success': False,
                'error': 'Site health check failed',
                'deploymentId': deployment_id,
                'health': health
            }
        
        print(f"✅ Site health verified")
        
        return {
            'success': True,
            'deploymentId': deployment_id,
            'url': f"https://{self.domain}",
            'health': health,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == '__main__':
    try:
        agent = DeployAgent()
        result = agent.deploy()
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['success'] else 1)
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)
```

---

## 5. Configuration

### 5.1 Environment Variables

```bash
# .env
COOLIFY_URL=http://localhost:8000
COOLIFY_WEBHOOK_URL=http://localhost:8000/api/webhooks/deploy/project-id/env-id
VERTICAL=A
DOMAIN=proqsmart.com
```

### 5.2 Requirements

```txt
requests==2.31.0
```

---

## 6. Testing

### 6.1 Unit Tests

```python
def test_trigger_deployment():
    agent = DeployAgent()
    agent.webhook_url = 'http://localhost:8000/api/webhooks/test'
    
    result = agent.trigger_deployment()
    
    assert 'id' in result
    assert result['status'] in ['queued', 'building', 'ready']
```

### 6.2 Integration Tests

```python
def test_full_deployment():
    agent = DeployAgent()
    
    result = agent.deploy()
    
    assert result['success'] is True
    assert result['deploymentId'] is not None
    assert result['url'].startswith('https://')
```

---

## 7. Error Handling

### 7.1 Deployment Failures

```python
def handle_deployment_failure(deployment_id: str):
    """Handle deployment failure with rollback"""
    
    # Get deployment logs
    logs = requests.get(f'{COOLIFY_URL}/api/deployments/{deployment_id}/logs')
    
    # Analyze failure
    if 'build failed' in logs.text:
        logger.error(f"Build failed: {logs.text}")
        # Notify developer
    elif 'health check failed' in logs.text:
        logger.error(f"Health check failed: {logs.text}")
        # Attempt rollback
        rollback_deployment(deployment_id)
    else:
        logger.error(f"Unknown deployment failure: {logs.text}")
```

### 7.2 Rollback

```python
def rollback_deployment(deployment_id: str):
    """Rollback to previous successful deployment"""
    
    response = requests.post(
        f'{COOLIFY_URL}/api/deployments/{deployment_id}/rollback',
        timeout=30
    )
    
    if response.status_code == 200:
        logger.info("Rollback successful")
    else:
        logger.error(f"Rollback failed: {response.text}")
```

---

## 8. Deployment Flow

### 8.1 Sequence Diagram

```
PM Agent → Hermes Deploy
    ↓
Hermes Deploy → Coolify Webhook
    ↓
Coolify → Git Pull (main)
    ↓
Coolify → Build (npm run build)
    ↓
Coolify → Deploy to Production
    ↓
Coolify → Health Check
    ↓
Hermes Deploy → Verify Site
    ↓
Hermes Deploy → Update Linear
    ↓
PM Agent → Notify Human
```

### 8.2 Example Output

```json
{
  "success": true,
  "deploymentId": "dep_123456",
  "url": "https://proqsmart.com",
  "health": {
    "healthy": true,
    "statusCode": 200,
    "responseTime": 245.3,
    "ssl": true
  },
  "timestamp": "2026-07-26T10:00:00Z"
}
```

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
