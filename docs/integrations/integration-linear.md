# Integration Specification: Linear

**Service:** Linear Task Management  
**Purpose:** Project tracking, task management, progress monitoring  
**Integration Type:** GraphQL API + TypeScript SDK  
**Free Tier:** 1000 issues/month (sufficient for MVP)  

---

## 1. Overview

Linear serves as the central task management system where all agent work is tracked, monitored, and reported. The Project Manager agent creates projects, assigns tasks to specialists, and updates progress in real-time.

---

## 2. Setup

### 2.1 Create Linear Account

1. Visit https://linear.app
2. Sign up for free account
3. Create team: "Marketing" (team ID will be generated)
4. Note team ID (e.g., "MAR")

### 2.2 Generate API Key

1. Go to Settings → API
2. Click "Create new API key"
3. Copy key (format: `lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
4. Store in environment variable: `LINEAR_API_KEY`

### 2.3 Install Dependencies

```bash
npm install @linear/sdk
```

### 2.4 Configure Environment

```bash
# .env
LINEAR_API_KEY=lin_api_xxx
LINEAR_TEAM_ID=MAR
LINEAR_WEBHOOK_SECRET=whsec_xxx  # Generated when creating webhook (see §5)
```

---

## 3. GraphQL API

### 3.1 Authentication

```typescript
import { LinearClient } from '@linear/sdk';

const client = new LinearClient({
  apiKey: process.env.LINEAR_API_KEY
});
```

### 3.2 Create Project

```graphql
mutation CreateIssue {
  createIssue(
    input: {
      title: "ProQSmart Content Q3 2026"
      teamId: "MAR"
      description: "Generate 20 leads/month from manufacturing SMEs"
      priority: 1  # 0=No priority, 1=Low, 2=Medium, 3=High, 4=Urgent
      stateId: "in-progress"
    }
  ) {
    success
    issue {
      id
      identifier
      url
    }
  }
}
```

### 3.3 Create Task

```graphql
mutation CreateSubtask {
  createIssue(
    input: {
      title: "Research manufacturing AI keywords"
      teamId: "MAR"
      parentId: "MAR-123"  # Parent project
      description: "Discover 50+ keywords with volume and difficulty"
      priority: 2
      assigneeId: "user-id"
    }
  ) {
    success
    issue {
      id
      identifier
    }
  }
}
```

### 3.4 Update Task Status

```graphql
mutation UpdateIssue {
  updateIssue(
    id: "MAR-124"
    input: {
      stateId: "done"
      description: """
      ✅ Research Complete
      
      **Keywords Discovered:** 50
      - Primary: 10 (avg volume: 2,100/mo)
      - Long-tail: 40 (avg volume: 650/mo)
      
      **Competitors Analyzed:** 5
      
      **Next:** Writer agent can start
      """
    }
  ) {
    success
  }
}
```

### 3.5 Add Comment

```graphql
mutation CreateComment {
  createComment(
    input: {
      issueId: "MAR-124"
      body: "⚠️ DataForSEO API rate limit reached, using cached data"
    }
  ) {
    success
    comment {
      id
      createdAt
    }
  }
}
```

### 3.6 Query Tasks

```graphql
query GetProjectTasks {
  team(id: "MAR") {
    issues(filter: {
      project: { id: { eq: "MAR-123" } }
    }) {
      nodes {
        id
        identifier
        title
        state {
          name
          color
        }
        createdAt
        updatedAt
      }
    }
  }
}
```

---

## 4. TypeScript SDK

### 4.1 Initialize Client

```typescript
import { LinearClient, Project, Issue } from '@linear/sdk';

const client = new LinearClient({
  apiKey: process.env.LINEAR_API_KEY
});
```

### 4.2 Create Project

```typescript
async function createProject(title: string, description: string) {
  const project = await client.createIssue({
    title,
    teamId: process.env.LINEAR_TEAM_ID,
    description,
    priority: 3,  // High
    stateId: 'in-progress'
  });
  
  return project.issue;
}

// Usage
const project = await createProject(
  'ProQSmart Content Q3 2026',
  'Generate 20 leads/month from manufacturing SMEs'
);
console.log(`Created ${project.identifier}: ${project.url}`);
```

### 4.3 Create Task

```typescript
async function createTask(parentId: string, title: string, description: string) {
  const task = await client.createIssue({
    title,
    teamId: process.env.LINEAR_TEAM_ID,
    parentId,
    description,
    priority: 2  // Medium
  });
  
  return task.issue;
}

// Usage
const task = await createTask(
  'MAR-123',
  'Research manufacturing AI keywords',
  'Discover 50+ keywords with volume and difficulty'
);
```

### 4.4 Update Task

```typescript
async function updateTask(taskId: string, updates: { stateId?: string; description?: string }) {
  const result = await client.updateIssue(taskId, updates);
  return result.success;
}

// Usage
await updateTask('MAR-124', {
  stateId: 'done',
  description: '✅ Research complete: 50 keywords discovered'
});
```

### 4.5 Get Tasks

```typescript
async function getProjectTasks(projectId: string) {
  const team = await client.team(process.env.LINEAR_TEAM_ID);
  const issues = await team.issues({
    filter: {
      project: { id: { eq: projectId } }
    }
  });
  
  return issues.nodes;
}

// Usage
const tasks = await getProjectTasks('MAR-123');
console.log(`Project has ${tasks.length} tasks`);
```

---

## 5. Webhooks

### 5.1 Setup Webhook

1. Go to Settings → Webhooks
2. Click "Create new webhook"
3. URL: `https://your-domain.com/api/webhooks/linear`
4. Events: Select "Issue" → "Update"
5. Copy webhook secret

### 5.2 Webhook Handler

```typescript
import express from 'express';
import crypto from 'crypto';

const app = express();

app.post('/api/webhooks/linear', async (req, res) => {
  // Verify webhook signature
  const signature = req.headers['linear-signature'];
  const body = JSON.stringify(req.body);
  
  const expectedSignature = crypto
    .createHmac('sha256', process.env.LINEAR_WEBHOOK_SECRET)
    .update(body)
    .digest('hex');
  
  if (signature !== expectedSignature) {
    return res.status(401).send('Invalid signature');
  }
  
  // Process webhook
  const { action, type, data } = req.body;
  
  if (type === 'Issue' && action === 'update') {
    const taskId = data.id;
    const newState = data.stateId;
    
    if (newState === 'done') {
      await onTaskComplete(taskId);
    } else if (newState === 'review') {
      await notifyHuman(`Task ${taskId} ready for review`);
    }
  }
  
  res.status(200).send('OK');
});
```

---

## 6. Project Structure

### 6.1 Recommended Structure

```
Linear Team: "Marketing" (MAR)
├── Project: "ProQSmart Content Q3 2026" (MAR-123)
│   ├── Goal: "Generate 20 leads/month"
│   ├── Tasks:
│   │   ├── MAR-124: Keyword Research (Researcher-A)
│   │   ├── MAR-125: Write 10 Articles (Writer-A)
│   │   ├── MAR-126: Design 5 Landing Pages (Designer-A)
│   │   ├── MAR-127: SEO Optimization (SEO-A)
│   │   └── MAR-128: Deploy to Production (Hermes-Deploy)
│   └── Status: In Progress
└── Project: "WeFab AI Content Q3 2026" (MAR-130)
    └── Status: Backlog
```

### 6.2 Task States

```
Backlog → Todo → In Progress → Review → Done
                ↑              ↓
                └──────┘ (Revisions)
```

**State IDs:**
- `backlog` - Backlog
- `todo` - Todo
- `in-progress` - In Progress
- `review` - Review
- `done` - Done

---

## 7. Best Practices

### 7.1 Task Naming

**Good:**
- "Research manufacturing AI keywords"
- "Write 10 pillar articles for ProQSmart"
- "Design landing pages for AI procurement"

**Bad:**
- "Do research"
- "Write stuff"
- "Design things"

### 7.2 Descriptions

**Include:**
- Clear objective
- Success criteria
- Links to relevant files
- Expected deliverables

**Example:**
```markdown
## Objective
Research and discover 50+ keywords for ProQSmart's AI procurement platform.

## Success Criteria
- 10+ primary keywords (volume >1000/mo)
- 40+ long-tail keywords (volume >100/mo)
- Competitor analysis for top 5 competitors
- Content gap analysis

## Deliverables
- keyword-strategy.json in workspace
- competitor-analysis.md
- industry-trends.md

## Links
- Linear Project: MAR-123
- Workspace: /root/.openclaw-pm/workspace-vertical-a/research/
```

### 7.3 Progress Updates

**Update frequency:** Every 6 hours or on milestone completion

**Example:**
```markdown
📊 Progress Update (6 hours)

✅ Completed:
- Keyword discovery: 50 keywords found
- Competitor analysis: 5 competitors analyzed

🟡 In Progress:
- Content gap analysis: 80% complete

⏳ Pending:
- Industry trends report

**Next:** Complete gap analysis in 2 hours
```

---

## 8. Error Handling

### 8.1 Rate Limits

**Linear API:** 1000 requests/minute

**Handling:**
```typescript
async function makeRequestWithRetry<T>(fn: () => Promise<T>): Promise<T> {
  const maxRetries = 3;
  let retryCount = 0;
  
  while (retryCount < maxRetries) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && retryCount < maxRetries - 1) {
        // Rate limited, wait and retry
        const waitTime = Math.pow(2, retryCount) * 1000;  // Exponential backoff
        await sleep(waitTime);
        retryCount++;
      } else {
        throw error;
      }
    }
  }
  
  throw new Error('Max retries exceeded');
}
```

### 8.2 Authentication Errors

**Detection:**
```typescript
try {
  const team = await client.team(process.env.LINEAR_TEAM_ID);
} catch (error) {
  if (error.message.includes('Authentication')) {
    logger.error('Linear API key invalid or expired');
    await notifyHuman('⚠️ Linear authentication failed');
  }
}
```

### 8.3 Webhook Security

**Best Practices:**
1. **Always verify signature** - Use `LINEAR_WEBHOOK_SECRET` to validate requests
2. **Use HTTPS** - Never expose webhook endpoint over HTTP
3. **Rotate secrets** - Regenerate webhook secret every 90 days
4. **Rate limit** - Limit webhook calls to prevent abuse
5. **Log failures** - Track invalid signatures for security monitoring

**Signature Verification:**
```typescript
const signature = req.headers['linear-signature'];
const expectedSignature = crypto
  .createHmac('sha256', process.env.LINEAR_WEBHOOK_SECRET)
  .update(body)
  .digest('hex');

if (signature !== expectedSignature) {
  logger.warn('Invalid webhook signature detected');
  return res.status(401).send('Invalid signature');
}
```

---

## 9. Testing

### 9.1 Unit Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('Linear Integration', () => {
  it('should create project', async () => {
    const project = await createProject('Test Project', 'Test Description');
    expect(project.id).toBeDefined();
    expect(project.title).toBe('Test Project');
  });
  
  it('should update task', async () => {
    const success = await updateTask('MAR-124', { stateId: 'done' });
    expect(success).toBe(true);
  });
});
```

### 9.2 Integration Tests

```typescript
describe('Linear Integration Tests', () => {
  it('full workflow', async () => {
    // 1. Create project
    const project = await createProject('Test Project', 'Test');
    
    // 2. Create task
    const task = await createTask(project.id, 'Test Task', 'Description');
    
    // 3. Update task
    await updateTask(task.id, { stateId: 'done' });
    
    // 4. Verify
    const tasks = await getProjectTasks(project.id);
    expect(tasks.length).toBe(1);
    expect(tasks[0].state.name).toBe('Done');
  });
});
```

---

## 10. Cost

| Tier | Price | Issues/Month | MVP Usage |
|------|-------|--------------|-----------|
| **Free** | $0 | 1000 | 500 issues (sufficient) |
| **Plus** | $8/user/mo | Unlimited | Not needed for MVP |
| **Pro** | $12/user/mo | Unlimited | Future scaling |

**MVP Cost:** $0 (Free tier sufficient)

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
