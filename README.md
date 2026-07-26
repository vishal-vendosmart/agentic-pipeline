# Agentic Pipeline — AI Content Generation System

**Automated SEO content generation and website management for ProQSmart and WeFab AI**

---

## 🎯 What This Is

A fully automated pipeline that:
- Generates SEO-optimized blog posts and landing pages
- Manages content in Payload CMS
- Deploys to production via Coolify
- Tracks all work in Linear
- Prevents hallucinations via Neo4j Knowledge Graph

**Result:** 10+ articles/month with <2 hours/week of human time

---

## 📚 Documentation

### Specifications
- **[Architecture Spec](docs/architecture-spec.md)** — System overview, agent roster, data flow
- **[Agent Specs](docs/agents/)** — Detailed specs for each agent
  - [Project Manager](docs/agents/agent-pm.md)
  - [Researcher](docs/agents/agent-researcher-a.md)
  - [Writer](docs/agents/agent-writer-a.md) (coming soon)
  - [Designer](docs/agents/agent-designer-a.md) (coming soon)
  - [SEO Specialist](docs/agents/agent-seo-a.md) (coming soon)
  - [Hermes CMS](docs/agents/agent-hermes-cms.md) (coming soon)
  - [Hermes Deploy](docs/agents/agent-hermes-deploy.md) (coming soon)
- **[Integration Specs](docs/integrations/)** — External system integrations
  - [Linear](docs/integrations/integration-linear.md) (coming soon)
  - [Neo4j](docs/integrations/integration-neo4j.md) (coming soon)
  - [OpenDesign](docs/integrations/integration-opendesign.md) (coming soon)
  - [Payload CMS](docs/integrations/integration-payload.md) (coming soon)
  - [Coolify](docs/integrations/integration-coolify.md) (coming soon)

---

## 🚀 Quick Start

### Prerequisites

- OpenClaw installed and configured
- Docker + Docker Compose
- Node.js 20+
- Python 3.11+

### 1. Clone Repository

```bash
git clone https://github.com/your-org/agentic-pipeline.git
cd agentic-pipeline
```

### 2. Install Dependencies

```bash
# Node.js dependencies
npm install

# Python dependencies
pip install -r requirements.txt
```

### 3. Set Up Services

```bash
# Start Neo4j
docker-compose up -d neo4j

# Start OpenDesign
docker-compose up -d opendesign

# Start Payload CMS
docker-compose up -d payload
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run Tests

```bash
npm test
```

---

## 🤖 Agent Roster (MVP)

| Agent | Role | Status |
|-------|------|--------|
| **Project Manager** | Your single interface, orchestrates all agents | ✅ Spec Complete |
| **Researcher (A)** | Discovers keywords, trends, competitors for ProQSmart | ✅ Spec Complete |
| **Writer (A)** | Generates SEO-optimized articles | 📝 In Progress |
| **Designer (A)** | Creates React/Tailwind designs | 📝 In Progress |
| **SEO (A)** | Optimizes content + technical SEO | 📝 In Progress |
| **Hermes CMS** | Syncs content to Payload CMS | 📝 In Progress |
| **Hermes Deploy** | Deploys to Coolify | 📝 In Progress |

---

## 🛠️ Tech Stack

**Orchestration:**
- OpenClaw (agent framework)
- Linear (task management)

**Data:**
- Neo4j (Knowledge Graph)
- DataForSEO (keyword research)
- SerpAPI (SERP analysis)

**Content:**
- Payload CMS (content management)
- OpenDesign (design generation)
- Gamma.app (infographics)

**Deployment:**
- Coolify (deployment automation)
- Hetzner EX44 (hosting)

---

## 📊 Implementation Phases

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Phase 1** | Week 1-2 | PM agent + Linear integration |
| **Phase 2** | Week 3 | Researcher agent + Neo4j KG |
| **Phase 3** | Week 4 | Writer agent |
| **Phase 4** | Week 5-6 | Designer agent + OpenDesign |
| **Phase 5** | Week 7 | SEO + Hermes agents |
| **Phase 6** | Week 8-10 | Polish + v2 prep |

---

## 💰 Cost Breakdown

| Service | Tier | Monthly Cost |
|---------|------|--------------|
| DataForSEO | Pay-per-use | ~$2.50 (5000 queries) |
| SerpAPI | Free | $0 (100 searches/mo) |
| Linear | Free | $0 (1000 issues/mo) |
| Neo4j | Self-hosted | $0 |
| OpenDesign | Self-hosted | $0 |
| Payload CMS | Self-hosted | $0 |
| Coolify | Self-hosted | $0 |
| Hetzner EX44 | VPS | €20 |
| **Total** | | **~$25/month** |

---

## 📈 Success Metrics

**MVP (Week 7):**
- 10 articles published for ProQSmart
- 5 landing pages live
- Zero hallucinations
- <2 hours/week human time
- <$50/month total cost

**v2 (Week 10):**
- 20 articles/month across both verticals
- Automated social posting
- <1 hour/week human time
- <$100/month total cost

---

## 🔧 Development

```bash
# Run tests
npm test

# Run linter
npm run lint

# Build docs
npm run docs

# Deploy specs
git add . && git commit -m "Update specs" && git push
```

---

## 📝 License

MIT — See [LICENSE](LICENSE) for details

---

## 🙋 Support

- **Documentation:** See `/docs` folder
- **Issues:** Open GitHub issue
- **Discussions:** GitHub Discussions

---

**Built for ProQSmart and WeFab AI**  
**Version:** 1.0  
**Last Updated:** 2026-07-26
