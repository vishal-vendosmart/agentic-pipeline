# How to Start the PM Agent

## ✅ OpenClaw is Ready

The PM agent is **registered and ready** in OpenClaw.

## Method 1: Start PM Agent Session

```bash
# Start a PM agent session
opencode --agent pm

# Or with a specific task
opencode --agent pm "Research keywords for AI procurement software"
```

## Method 2: Use CLI (Already Working)

```bash
cd /root/dev/agentic-pipeline

# Quick research
./pm-cli.sh research

# Check status
./pm-cli.sh status

# List keywords
./pm-cli.sh keywords
```

## What the PM Agent Can Do

Once started, the PM agent will:

1. **Create Linear projects** - Uses Linear MCP tools
2. **Spawn Hermes agents** - Via `exec` tool
   - Researcher: `/root/.openclaw/hermes-agents/researcher-vertical-a/agent.py`
   - Writer: (TODO)
   - Designer: (TODO)
3. **Track progress** - Updates Linear tasks
4. **Log work** - Updates IMPLEMENTATION.md and journal

## Example Session

```
You: Research keywords for "AI procurement software"

PM Agent:
1. ✅ Creating Linear task MAR-254...
2. 🚀 Spawning researcher agent...
3. ⏳ Waiting for completion...
4. ✅ Research complete: 12 keywords found
5. 📝 Updating Linear task with results
6. 💾 Keywords stored in Neo4j

Done! Check Linear task MAR-254 for details.
```

## Verify It's Working

```bash
# Check agent is registered
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); print([a['id'] for a in d['agents']['list']])"

# Should output: ['main', 'writer', 'pm']
```

## Configuration

- **Agent ID:** `pm`
- **Agent Name:** `pm-agent`
- **Workspace:** `/root/.openclaw/workspace-pm`
- **Model:** `ollama-cloud/minimax-m3`
- **System Prompt:** `/root/.openclaw/agents/pm-agent/system.md`
- **Config:** `/root/.openclaw/agents/pm-agent/config.json`

## Next Steps

1. Start PM agent: `opencode --agent pm`
2. Give it a task: "Research 10 keywords for manufacturing AI"
3. Watch it work in Linear and Neo4j
