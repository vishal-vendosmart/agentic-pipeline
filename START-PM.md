# How to Start the PM Agent

## Architecture (fully isolated from Milo)

PM Agent runs in its **own OpenClaw profile** — completely separate from Milo.
Same pattern as Milo: openclaw runtime state in the profile dir, **content lives in the project repo** via symlinks.

| | Milo (marketing) | PM Agent (pipeline) |
|---|---|---|
| State home | `/root/.openclaw` | `/root/.openclaw-pm` |
| Content (symlinked) | `/opt/marketing-stack/dev/workspace` | `/root/dev/agentic-pipeline/workspace` |
| Gateway port | 18789 | 18790 |
| systemd unit | `openclaw-gateway.service` | `openclaw-pm-gateway.service` |
| Telegram bot | `@Proqsmart_agent_bot` | `@ProQsmart_pm_bot` |
| Agents | main, writer | pm-agent (only) |

PM's symlinks: `/root/.openclaw-pm/{workspace, hermes-agents, workspace-vertical-a}` → `/root/dev/agentic-pipeline/`

There is **no shared config, no shared bot, no routing between them**.

## Method 1: Telegram (primary)

DM **@ProQsmart_pm_bot** on Telegram. PM's gateway polls it directly.

## Method 2: CLI chat via PM's gateway

```bash
openclaw --profile pm agents chat pm-agent
```

## Method 3: Pipeline CLI (direct, no gateway)

```bash
cd /root/dev/agentic-pipeline

./pm-cli.sh research   # Run keyword research pipeline
./pm-cli.sh status     # Neo4j database status
./pm-cli.sh keywords   # List keywords in Neo4j
```

## Service management

```bash
systemctl status openclaw-pm-gateway   # status
journalctl -u openclaw-pm-gateway -f   # logs
systemctl restart openclaw-pm-gateway  # restart
```

## Verify installation

```bash
openclaw --profile pm agents list
# Should show ONLY: pm-agent (default)

# Milo's side must show ONLY main + writer:
openclaw agents list
```

## Configuration

- **Agent ID:** `pm-agent`
- **Workspace:** `/root/dev/agentic-pipeline/workspace` (symlinked from `/root/.openclaw-pm/workspace`)
- **Agent dir:** `/root/.openclaw-pm/agents/pm-agent/agent` (system.md, IDENTITY.md)
- **Config:** `/root/.openclaw-pm/openclaw.json`
- **Model:** `ollama-cloud/minimax-m3` (fallback: `deepseek-v4-pro`)
- **Hermes agents:** `/root/dev/agentic-pipeline/hermes-agents/` (researcher-vertical-a installed; writer/designer/seo TODO)
- **Research output:** `/root/dev/agentic-pipeline/workspace-vertical-a/`
- **Data:** Neo4j container `agentic-pipeline-neo4j` (localhost:7474/:7687)
