# Agentic Pipeline — Usage Guide

## Architecture (3 independent agents)

| Agent | Gateway | Profile | Reachable via |
|-------|---------|---------|---------------|
| pm-agent | :18790 | ~/.openclaw-pm | Telegram (@ProQsmart_pm_bot), CLI |
| researcher-a | :18793 | ~/.openclaw-researcher-a | A2A from PM, CLI, heartbeat |
| writer-a | :18794 | ~/.openclaw-writer-a | A2A from PM, CLI, heartbeat |

**Coordination:** PM dispatches via A2A (`openclaw --profile <target> agent --json`) + Linear task bus (labeled issues). Each agent's heartbeat polls Linear every 10m for labeled tasks.

## 1. Telegram (PM Agent — user-facing)

DM **@ProQsmart_pm_bot** with a content request (keyword, topic, or brief). PM will:
1. Create a Linear tracking issue
2. A2A researcher-a for keyword research
3. A2A writer-a for article draft
4. Report results back to you

## 2. CLI — direct agent interaction

```bash
# PM Agent
openclaw --profile pm agent --agent pm-agent -m "Research AI procurement keywords and write an article"

# Researcher-A directly
openclaw --profile researcher-a agent --agent researcher-a -m "Research keywords for: AI procurement software"

# Writer-A directly
openclaw --profile writer-a agent --agent writer-a -m "Write an article about AI procurement software for SMEs"
```

## 3. Pipeline CLI (batch utilities — NOT agents)

```bash
cd /root/dev/agentic-pipeline

./pm-cli.sh research    # Run keyword research utility directly
./pm-cli.sh status      # Neo4j database status
./pm-cli.sh keywords    # List keywords in Neo4j
```

## 4. Service management

```bash
# All 3 gateways
systemctl status openclaw-pm-gateway openclaw-researcher-a-gateway openclaw-writer-a-gateway
journalctl -u openclaw-pm-gateway -f          # PM logs
journalctl -u openclaw-researcher-a-gateway -f # Researcher logs
journalctl -u openclaw-writer-a-gateway -f     # Writer logs
```

## 5. Linear task bus

PM creates issues labeled `agent:researcher-a` or `agent:writer-a`. Each agent's heartbeat polls for its label. Check status:

```bash
openclaw --profile pm agent --agent pm-agent -m "What's the status of the pipeline?"
```

## Configuration

- **Repo:** `/root/dev/agentic-pipeline/`
- **PM config:** `/root/.openclaw-pm/openclaw.json`
- **Researcher config:** `/root/.openclaw-researcher-a/openclaw.json`
- **Writer config:** `/root/.openclaw-writer-a/openclaw.json`
- **Utilities:** `/root/dev/agentic-pipeline/utilities/` (deterministic scripts, NOT agents)
- **Data:** Neo4j (`agentic-pipeline-neo4j` container, localhost:7474/:7687)
- **Linear:** team MAR (`6708e155-7999-4102-994c-88e6cdc1180f`)
