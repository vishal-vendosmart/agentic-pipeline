# Agent Specification: Project Manager

**ID:** `project-manager`  
**Role:** Strategic Partner + Orchestrator  
**Vertical:** Both (ProQSmart + WeFab AI)  
**Primary Model:** `ollama-cloud/minimax-m3`  
**Workspace:** `/root/.openclaw-pm/workspace-pm/`

---

## 1. Purpose

Serve as the single interface between you and the agentic system. Translates business objectives into Linear projects, orchestrates specialist agents, and tracks progress via Linear task updates.

---

## 2. Inputs

### 2.1 From Human

**Format:** Telegram message or CLI command

**Examples:**
```
Telegram: "Generate 20 qualified leads per month from manufacturing SMEs"
CLI: openclaw spawn project-manager --task "Build ProQSmart content pipeline"
```

**Expected Input Structure:**
```json
{
  "objective": "Generate 20 leads/month from manufacturing SMEs",
  "vertical": "A",
  "timeline": "90 days",
  "budget": "$100/month",
  "constraints": ["focus on SEO", "no paid ads"]
}
```

### 2.2 From Linear

**Format:** GraphQL API responses

**Data Received:**
- Task status updates (In Progress → Review → Done)
- Agent work logs
- Completion notifications
- Blocker alerts

---

## 3. Outputs

### 3.1 To Linear

**Operations:**
- Create projects: `createIssue` mutation
- Create tasks: `createIssue` with parent relationship
- Update status: `UpdateIssueInput` mutation
- Add comments: `CreateCommentInput` mutation
- Upload files: `createAttachmentUrl` mutation

**Example - Create Project:**
```graphql
mutation {
  createIssue(
    input: {
      title: "ProQSmart Content Q3 2026"
      teamId: "MAR"
      description: "Generate 20 leads/month from manufacturing SMEs"
      priority: Priority.High
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

**Example - Update Task Status:**
```graphql
mutation {
  updateIssue(
    id: "MAR-123"
    input: {
      stateId: "done"
      description: "✅ Research complete: 50 keywords discovered"
    }
  ) {
    success
  }
}
```

### 3.2 To Specialist Agents

**Format:** `sessions_spawn` tool calls

**Example:**
```json
{
  "agentId": "researcher-vertical-a",
  "task": "Research manufacturing AI keywords",
  "params": {
    "objective": "Generate 20 leads/month",
    "vertical": "A",
    "linearTaskId": "MAR-124"
  },
  "context": "isolated"
}
```

### 3.3 To Human

**Format:** Telegram notifications

**Examples:**
```
✅ Project Created: "ProQSmart Content Q3 2026"
   Linear: https://linear.app/proqsmart/issue/MAR-123
   
📊 Progress Update: 3/10 tasks complete
   - Research: ✅ Done
   - Writing: 🟡 In Progress (2/10)
   - Design: ⏳ Pending
   
⚠️ Blocker: Designer agent timeout
   Task: MAR-126 (Landing page design)
   Action: /retry MAR-126 or /reassign MAR-126
```

---

## 4. Behaviors

### 4.1 Objective Intake Workflow

**Step 1: Parse Objective**
```python
def parse_objective(human_message: str) -> dict:
    # Extract: goal, vertical, timeline, constraints
    # Validate: goal is measurable, vertical exists
    return {
        "goal": "Generate 20 leads/month",
        "vertical": "A",
        "timeline_days": 90,
        "constraints": ["SEO focus", "no paid ads"]
    }
```

**Step 2: Query Knowledge Graph**
```cypher
// Check existing objectives
MATCH (o:Objective {vertical: "A"})
RETURN o.goal, o.status, o.createdAt

// Check current state
MATCH (c:Content)-[:TARGETS]->(:Vertical {id: "A"})
RETURN count(c) as content_count, avg(c.wordCount) as avg_words
```

**Step 3: Create Linear Project**
```typescript
const project = await linear.createIssue({
  title: `ProQSmart Content ${getQuarter()}`,
  description: objective.goal,
  priority: 'High',
  teamId: 'MAR'
});
```

**Step 4: Break Down into Tasks**
```python
tasks = [
    {"name": "Keyword Research", "agent": "researcher-vertical-a", "estimate": "2 days"},
    {"name": "Write 10 Pillar Articles", "agent": "writer-vertical-a", "estimate": "5 days"},
    {"name": "Design 5 Landing Pages", "agent": "designer-vertical-a", "estimate": "3 days"},
    {"name": "SEO Optimization", "agent": "seo-vertical-a", "estimate": "2 days"},
    {"name": "Deploy to Production", "agent": "hermes-deploy", "estimate": "1 day"}
]
```

**Step 5: Spawn Specialists**
```python
for task in tasks:
    await sessions_spawn(
        agentId=task["agent"],
        task=task["name"],
        params={"linearTaskId": task["id"], "objective": objective}
    )
```

### 4.2 Progress Monitoring Workflow

**Every 6 hours:**
```python
# Query Linear for task status
tasks = await linear.query("""
  MATCH (t:Task)-[:BELONGS_TO]->(p:Project {id: $projectId})
  RETURN t.name, t.state, t.updatedAt
""")

# Calculate progress
completed = sum(1 for t in tasks if t.state == "done")
total = len(tasks)
progress_pct = (completed / total) * 100

# If stalled, investigate
if any(t.state == "in_progress" and t.updatedAt < 24h for t in tasks):
    await notify_human(f"⚠️ Task {t.name} stalled for 24h")
```

### 4.3 Reporting Workflow

**Daily Report (9 AM Helsinki):**
```
📊 Daily Progress Report - ProQSmart Content

✅ Completed (2):
   - Keyword Research (MAR-124)
   - Homepage Draft (MAR-125)

🟡 In Progress (3):
   - Blog Post 1: "AI in Manufacturing" (MAR-126) - 60%
   - Landing Page Design (MAR-127) - 30%
   - SEO Audit (MAR-128) - 10%

⏳ Pending (5):
   - Blog Posts 2-10
   - Deployment

📈 Metrics:
   - Keywords Discovered: 50
   - Content Created: 2 articles
   - Avg Word Count: 2150
   - Estimated Launch: 3 days

🔗 Linear: https://linear.app/proqsmart/project/MAR
```

---

## 5. Tools Required

### 5.1 OpenClaw Tools

| Tool | Permission | Purpose |
|------|------------|---------|
| `sessions_spawn` | Allow | Spawn specialist agents |
| `sessions_send` | Allow | Send messages to agents |
| `read` | Allow | Read workspace files |
| `write` | Allow | Write reports, state files |
| `exec` | Allow | Run Linear SDK scripts |

### 5.2 External APIs

| API | Method | Purpose |
|-----|--------|---------|
| **Linear GraphQL** | `createIssue`, `updateIssue`, `createComment` | Task management |
| **Linear TypeScript SDK** | `LinearClient` | Programmatic access |
| **Neo4j Bolt** | Cypher queries | Query objectives, state |

### 5.3 Python Dependencies

```txt
@linear/sdk          # Linear API client
neo4j                # Neo4j driver
python-telegram-bot  # Telegram notifications
```

---

## 6. Configuration

### 6.1 Environment Variables

```bash
# Linear
LINEAR_API_KEY=lin_api_xxx
LINEAR_TEAM_ID=MAR

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Telegram
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=8783680298

# OpenClaw
OPENCLAW_GATEWAY_URL=http://localhost:18789
OPENCLAW_TOKEN=xxx
```

### 6.2 Model Configuration

```json
{
  "model": {
    "primary": "ollama-cloud/minimax-m3",
    "fallbacks": ["ollama-cloud/deepseek-v4-pro"],
    "thinkingDefault": "high",
    "reasoningDefault": "on",
    "timeoutSeconds": 300
  }
}
```

### 6.3 Subagent Configuration

```json
{
  "subagents": {
    "maxConcurrent": 5,
    "maxChildrenPerAgent": 10,
    "runTimeoutSeconds": 1800,
    "allowAgents": [
      "researcher-vertical-a",
      "writer-vertical-a",
      "designer-vertical-a",
      "seo-vertical-a",
      "hermes-cms-sync",
      "hermes-deploy"
    ]
  }
}
```

---

## 7. Testing

### 7.1 Unit Tests

**Test: Objective Parsing**
```python
def test_parse_objective():
    input = "Generate 20 leads/month from manufacturing SMEs"
    result = parse_objective(input)
    assert result["goal"] == "Generate 20 leads/month"
    assert result["vertical"] == "A"
```

**Test: Linear Project Creation**
```python
def test_create_linear_project():
    project = pm.create_project("Test Project", "Test Goal")
    assert project.id is not None
    assert project.teamId == "MAR"
    # Cleanup
    await linear.deleteIssue(project.id)
```

### 7.2 Integration Tests

**Test: Full Workflow**
```python
async def test_full_workflow():
    # 1. Create objective
    await pm.handle_objective("Generate 5 leads this week")
    
    # 2. Verify Linear project created
    project = await linear.getProject("Generate 5 leads")
    assert project is not None
    
    # 3. Verify tasks created
    tasks = await linear.getTasks(project.id)
    assert len(tasks) >= 5
    
    # 4. Wait for completion (timeout: 10 minutes)
    await wait_for_completion(project.id, timeout=600)
    
    # 5. Verify all tasks done
    final_tasks = await linear.getTasks(project.id)
    assert all(t.state == "done" for t in final_tasks)
```

### 7.3 Success Criteria

- ✅ Creates Linear project within 30 seconds of objective
- ✅ Spawns all specialist agents within 2 minutes
- ✅ Updates Linear task status in real-time
- ✅ Sends daily progress report at 9 AM Helsinki
- ✅ Detects stalled tasks within 24 hours
- ✅ Zero orphaned tasks (all tasks have owners)

---

## 8. Error Handling

### 8.1 Agent Spawn Failures

**Scenario:** Specialist agent fails to spawn

**Detection:**
```python
try:
    await sessions_spawn(agentId="researcher-vertical-a", ...)
except SpawnError as e:
    await linear.addComment(taskId, f"❌ Failed to spawn agent: {e}")
    await notify_human(f"⚠️ Agent spawn failed: {e}")
```

**Recovery:**
1. Retry spawn (max 3 attempts)
2. If still failing, reassign to backup agent
3. Log to Linear task comments

### 8.2 Linear API Failures

**Scenario:** Linear API rate limit or timeout

**Detection:**
```python
try:
    await linear.createIssue(...)
except RateLimitError:
    # Handle rate limit
except TimeoutError:
    # Handle timeout
```

**Recovery:**
1. Exponential backoff (1s, 2s, 4s, 8s)
2. Queue task for later
3. Notify human if >5 failures

### 8.3 Objective Drift Detection

**Scenario:** Agent outputs don't align with objective

**Detection:**
```python
def check_alignment(output: str, objective: str) -> bool:
    # Query KG for objective
    kg_objective = await neo4j.query("MATCH (o:Objective) RETURN o.goal")
    
    # Simple alignment check (can use LLM for better accuracy)
    return objective.lower() in output.lower()
```

**Recovery:**
1. Flag task for human review
2. Pause agent
3. Request clarification from human

---

## 9. Linear Integration Details

### 9.1 Project Structure

```
Linear Team: "Marketing" (MAR)
├── Project: "ProQSmart Content Q3 2026" (MAR-123)
│   ├── Goal: "Generate 20 leads/month"
│   ├── Tasks:
│   │   ├── MAR-124: Keyword Research (Researcher-A)
│   │   ├── MAR-125: Write Homepage (Writer-A)
│   │   ├── MAR-126: Write 10 Blog Posts (Writer-A)
│   │   ├── MAR-127: Design Landing Pages (Designer-A)
│   │   ├── MAR-128: SEO Optimization (SEO-A)
│   │   └── MAR-129: Deploy to Production (Hermes-Deploy)
│   └── Status: In Progress
└── Project: "WeFab AI Content Q3 2026" (MAR-130)
    └── Status: Backlog
```

### 9.2 Task State Machine

```
Backlog → Todo → In Progress → Review → Done
                ↑              ↓
                └──────┘ (Revisions)
```

**State Transitions:**
- `Backlog → Todo`: PM assigns task
- `Todo → In Progress`: Agent starts work
- `In Progress → Review`: Agent completes work
- `Review → Done`: Human approves
- `Review → In Progress`: Human requests revisions

### 9.3 Webhook Handlers

**Endpoint:** `POST /api/webhooks/linear`

**Events:**
```json
{
  "action": "update",
  "type": "Issue",
  "data": {
    "id": "MAR-124",
    "stateId": "done",
    "updatedAt": "2026-07-26T10:00:00Z"
  }
}
```

**Handler:**
```python
@app.post("/api/webhooks/linear")
async def handle_linear_webhook(event: dict):
    if event["type"] == "Issue" and event["action"] == "update":
        task_id = event["data"]["id"]
        new_state = event["data"]["stateId"]
        
        if new_state == "done":
            await pm.on_task_complete(task_id)
        elif new_state == "review":
            await pm.notify_human(f"Task {task_id} ready for review")
```

---

## 10. Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Task Creation Latency** | <30 seconds | Time from objective to Linear project |
| **Agent Spawn Success Rate** | 99%+ | Successful spawns / Total spawns |
| **Task Completion Rate** | 95%+ | Completed tasks / Total tasks |
| **Stalled Task Detection** | <24 hours | Time from stall to detection |
| **Human Notification Latency** | <5 minutes | Time from event to notification |
| **Daily Report Accuracy** | 100% | Reports sent on time / Total days |

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: After Phase 1 implementation*
