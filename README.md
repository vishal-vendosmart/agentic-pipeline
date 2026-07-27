# Agentic Pipeline — AI Content Generation System

**Automated SEO content generation for ProQSmart and WeFab AI**

---

## What This Is

A pipeline of independent OpenClaw agents that:
- Researches real keywords via live DataForSEO API
- Writes SEO articles grounded in domain knowledge
- Tracks all work in Linear (task bus + audit trail)
- Stores project truth in Neo4j (startup identity, market data, transactions)
- Deploys content to production (future: Payload CMS + Coolify)

**Target:** 10+ articles/month with <2 hours/week of human time, <$50/month cost

---

## Agent Status

| Agent | Role | Status | Gateway |
|-------|------|--------|---------|
| **pm-agent** | Orchestrator + user interface | ✅ Live | :18790 |
| **researcher-a** | Live keyword research (DataForSEO) | ✅ Live | :18793 |
| **writer-a** | SEO article drafts | ✅ Live | :18794 |
| **designer-a** | Landing page design | ❌ Not built | — |
| **seo-a** | Content + technical SEO | ❌ Not built | — |
| **hermes-cms** | Payload CMS sync | ❌ Not built | — |
| **hermes-deploy** | Coolify deployment | ❌ Not built | — |

Each agent is a **real OpenClaw agent** — own profile, own gateway, own heartbeat. No sub-agents, no scripts disguised as agents. Coordination via A2A (cross-gateway) + Linear task bus.

---

## Documentation

- **[Architecture Spec](docs/architecture-spec.md)** — System overview, §6.4 Agent Installation Standard
- **[Agent Specs](docs/agents/)** — PM, Researcher-A, Writer-A, Designer-A, SEO-A, Hermes-CMS, Hermes-Deploy
- **[Integration Specs](docs/integrations/)** — Linear, Neo4j, DataForSEO, SerpAPI, OpenDesign, Payload, Coolify, Gamma, Zernio
- **[PLAN.md](PLAN.md)** — 8-week MVP plan + progress
- **[START-PM.md](START-PM.md)** — How to start/use the pipeline
- **[USAGE.md](USAGE.md)** — Full usage guide

---

## Quick Start

### Prerequisites

- OpenClaw installed (`/opt/node24/`)
- Docker + Docker Compose
- Python 3.11+

### 1. Clone

```bash
git clone https://github.com/vishal-vendosmart/agentic-pipeline.git
cd agentic-pipeline
```

### 2. Start Neo4j

```bash
docker-compose up -d neo4j
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env with your API keys (Linear, DataForSEO, Neo4j, Ollama)
```

### 4. Start the agents

```bash
systemctl start openclaw-pm-gateway openclaw-researcher-a-gateway openclaw-writer-a-gateway
```

### 5. Use it

DM **@ProQsmart_pm_bot** on Telegram, or via CLI:

```bash
openclaw --profile pm agent --agent pm-agent -m "Research and write an article about AI procurement software"
```

---

## Tech Stack

- **Agents:** OpenClaw (3 independent gateways, A2A + Linear bus)
- **Task management:** Linear (team MAR, labeled issues)
- **Knowledge graph:** Neo4j (project truth: startup identity, ICP, keywords, competitors)
- **Keyword research:** DataForSEO Labs (live API, ~$0.04/run)
- **LLM:** Ollama Cloud (minimax-m3, $0)
- **Content:** Markdown drafts → Payload CMS (future) → Coolify deploy (future)

---

## Cost

| Service | Budget | Current |
|---------|--------|---------|
| DataForSEO | ~$2.50/mo | ~$0.15 spent |
| Ollama Cloud | $0 | $0 |
| Linear | $0 (free) | $0 |
| Neo4j | $0 (self-hosted) | $0 |
| **Total** | **~$25/mo** | **~$0.15** |

---

## Repository

- **GitHub:** https://github.com/vishal-vendosmart/agentic-pipeline
- **Branch:** development
- **Visibility:** Public