# PM Agent - Usage Guide

## How to Interact with the PM Agent

### 1. **CLI (Recommended for Quick Testing)**

```bash
cd /root/dev/agentic-pipeline

# Run keyword research
./pm-cli.sh research

# Check Neo4j status
./pm-cli.sh status

# List keywords
./pm-cli.sh keywords
```

### 2. **OpenClaw Session (Full Integration)**

Start an OpenClaw session with the PM agent:

```bash
# The PM agent runs in its own isolated profile: /root/.openclaw-pm/openclaw.json
# Start it with: openclaw --profile pm agents chat pm-agent (or DM @ProQsmart_pm_bot)
# It has access to:
# - Linear MCP tools (create/update tasks)
# - exec tool (spawn Hermes agents)
# - read/write (workspace management)

# In your OpenClaw session, you can:
1. Create Linear projects
2. Spawn researcher: exec python3 /root/.openclaw-pm/hermes-agents/researcher-a/research.py
3. Track progress in Linear
```

### 3. **REST API (For Web UIs)**

```bash
# Install Flask
pip install flask

# Start API server
python3 /root/dev/agentic-pipeline/pm-api.py

# Use endpoints:
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["AI software"]}'

curl http://localhost:8080/status

curl http://localhost:8080/keywords
```

### 4. **Telegram Bot (Mobile/Chat)**

```bash
# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Run bot
python3 /root/dev/agentic-pipeline/pm-telegram.py research
```

---

## Architecture

```
User Interface (CLI/API/Telegram/OpenClaw)
         ↓
PM Agent (agents/pm/agent.py)
         ↓
Spawns via exec → Hermes Researcher (/root/.openclaw-pm/hermes-agents/researcher-vertical-a/)
         ↓                                    ↓
Linear MCP Tools                    Neo4j (store keywords)
```

---

## Available Commands

| Command | Interface | Description |
|---------|-----------|-------------|
| `research` | All | Run keyword research pipeline |
| `status` | CLI, API | Show Neo4j database status |
| `keywords` | CLI, API | List keywords in Neo4j |
| `create-project` | OpenClaw | Create Linear project |
| `spawn-writer` | OpenClaw | Spawn Writer agent (TODO) |

---

## Example: Full Workflow via CLI

```bash
# 1. Start research
./pm-cli.sh research

# 2. Check results
./pm-cli.sh status
./pm-cli.sh keywords

# 3. Verify in Neo4j Browser
# Open http://localhost:7474
# Run: MATCH (k:Keyword) RETURN k.term, k.volume ORDER BY k.volume DESC
```

---

## Configuration

**Environment Variables (.env):**
```bash
LINEAR_TEAM_ID=6708e155-7999-4102-994c-88e6cdc1180f
NEO4J_PASSWORD=Agentic2026SecurePass
DATAFORSEO_EMAIL=vishal@proqsmart.com
DATAFORSEO_PASSWORD=a25b69e4ad3fbbb2
```

**Hermes Agents:**
- Researcher: `/root/.openclaw-pm/hermes-agents/researcher-vertical-a/`
- Writer: (TODO)
- Designer: (TODO)

**Neo4j:**
- Browser: http://localhost:7474
- Bolt: localhost:7687
- Password: `Agentic2026SecurePass`

---

## Next Steps

1. **Make DataForSEO live** - Add $1 deposit for real API access
2. **Implement Writer agent** - Create Hermes writer agent
3. **OpenClaw integration** - Test sessions_spawn from PM to Hermes
4. **Add Telegram bot** - Configure bot token for chat interface
