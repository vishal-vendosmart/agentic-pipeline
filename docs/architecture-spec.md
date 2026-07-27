# Architecture Specification: AI Content Pipeline

**Version:** 1.0  
**Created:** 2026-07-26  
**Status:** Ready for Implementation  

---

## 1. Executive Summary

This document defines the architecture for an automated AI content generation and website management pipeline. The system uses **OpenClaw** for agent orchestration, **Linear** for task management, **Neo4j** for knowledge grounding, and integrates with multiple external services for SEO, design, and deployment.

### 1.1 Business Context

**Vertical A (MVP): ProQSmart**
- Smart procurement platform for manufacturing SMEs
- Goal: Generate 20 qualified leads/month
- Domain: proqsmart.com / proqsmart.app

**Vertical B (v2): WeFab AI**
- AI-powered manufacturing marketplace
- Domain: wefab.ai

### 1.2 System Goals

**Primary Objectives:**
1. Reduce content generation time from 20+ hours/week to <2 hours/week
2. Generate SEO-optimized content that ranks in top 3 for target keywords
3. Maintain fact-grounded output with zero hallucinations
4. Single interface (Project Manager agent) for human oversight
5. Linear-based task tracking for full visibility

**Success Metrics:**
- 10+ articles published/month per vertical
- Core Web Vitals: All green (LCP <2.5s, FID <100ms, CLS <0.1)
- Linear task completion rate: 95%+
- Zero hallucinated facts in published content

---

## 2. Architecture Overview

### 2.1 High-Level Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    HUMAN INTERFACE                           │
│                                                              │
│  You → Project Manager Agent (Telegram/Linear)              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 LINEAR TASK MANAGEMENT                       │
│                                                              │
│  Projects, Tasks, Status Updates, Notifications             │
│  All agents report work to Linear                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 OPENCLAW ORCHESTRATION                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         PROJECT MANAGER AGENT                         │  │
│  │  - Receives business objectives                       │  │
│  │  - Creates Linear projects/tasks                      │  │
│  │  - Spawns specialist agents                           │  │
│  │  - Tracks progress via Linear                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↓                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ RESEARCHER  │  │   WRITER    │  │  DESIGNER   │        │
│  │  (x2)       │  │   (x2)      │  │   (x2)      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │  SEO (x2)   │  │   HERMES    │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              KNOWLEDGE GRAPH (Neo4j)                         │
│                                                              │
│  - Objectives, Facts, Keywords, Competitors                 │
│  - All agents query before output                           │
│  - Prevents hallucinations                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL INTEGRATIONS                        │
│                                                              │
│  DataForSEO → Keyword research                              │
│  SerpAPI    → SERP analysis                                  │
│  OpenDesign → Design generation                              │
│  Payload    → CMS management                                 │
│  Coolify    → Deployment automation                          │
│  Zernio     → Social media posting                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Agent Roster

### 3.1 MVP Agents (7 Total)

| ID | Role | Vertical | Primary Model | Key Tools |
|----|------|----------|---------------|-----------|
| `project-manager` | Strategic PM + Orchestrator | Both | minimax-m3 | Linear SDK, sessions_spawn |
| `researcher-vertical-a` | Keyword/trend discovery | ProQSmart | minimax-m3 | DataForSEO, SerpAPI, Neo4j |
| `writer-vertical-a` | Content generation | ProQSmart | gemma4:31b | Neo4j, Zernio |
| `designer-vertical-a` | UI/UX design + code | ProQSmart | minimax-m3 | OpenDesign, Gamma.app |
| `seo-vertical-a` | Content + technical SEO | ProQSmart | minimax-m3 | DataForSEO, Lighthouse |
| `hermes-cms-sync` | Payload CMS integration | Both | Python | Payload API |
| `hermes-deploy` | Coolify deployment | Both | Python | Coolify webhooks |

### 3.2 v2 Agents (4 Additional)

| ID | Role | Vertical | Notes |
|----|------|----------|-------|
| `researcher-vertical-b` | Keyword/trend discovery | WeFab AI | Same as Vertical A |
| `writer-vertical-b` | Content generation | WeFab AI | Same as Vertical A |
| `designer-vertical-b` | UI/UX design + code | WeFab AI | Same as Vertical A |
| `seo-vertical-b` | Content + technical SEO | WeFab AI | Same as Vertical A |

---

## 4. Data Flow

### 4.1 Content Generation Flow

```
1. Human → PM Agent: "Generate 20 leads/month from manufacturing SMEs"
2. PM Agent → Linear: Create project "ProQSmart Content Q3"
3. PM Agent → Researcher-A: Spawn task "Research manufacturing AI keywords"
4. Researcher-A → DataForSEO: Query keyword volumes
5. Researcher-A → SerpAPI: Get SERP analysis
6. Researcher-A → Neo4j: Write discovered keywords + facts
7. Researcher-A → Linear: Update task "Research complete"
8. PM Agent → Writer-A: Spawn task "Write 5 pillar articles"
9. Writer-A → Neo4j: Query keywords + facts
10. Writer-A → Workspace: Write markdown drafts
11. Writer-A → Linear: Update task "Drafts complete"
12. PM Agent → Designer-A: Spawn task "Design landing pages"
13. Designer-A → OpenDesign: Generate React components
14. Designer-A → Workspace: Write .tsx files
15. Designer-A → Linear: Update task "Design complete"
16. PM Agent → SEO-A: Spawn task "Optimize for search"
17. SEO-A → DataForSEO: Check rankings
18. SEO-A → Workspace: Add meta tags, schema
19. SEO-A → Linear: Update task "SEO complete"
20. PM Agent → Hermes-CMS: Spawn "Sync to Payload"
21. Hermes-CMS → Payload: POST content
22. Hermes-CMS → Linear: Update task "CMS sync complete"
23. PM Agent → Hermes-Deploy: Spawn "Deploy to production"
24. Hermes-Deploy → Coolify: Trigger webhook
25. Hermes-Deploy → Linear: Update task "DEPLOYED ✅"
```

### 4.2 Knowledge Graph Flow

```
┌─────────────┐
│   Human     │
│  Objective  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     PM      │
│   Creates   │
│  Objective  │
│   in KG     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Researcher │
│  Discovers  │
│  Keywords   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Writer    │
│   Queries   │
│   KG for    │
│   Facts     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Designer   │
│  Queries KG │
│  for Brand  │
│  Guidelines │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     SEO     │
│   Queries   │
│   KG for    │
│   Rankings  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Publish   │
│   + Store   │
│   Results   │
│   in KG     │
└─────────────┘
```

---

## 5. External Integrations

### 5.1 API Matrix

| Service | Purpose | Free Tier | Paid Tier | MVP Usage |
|---------|---------|-----------|-----------|-----------|
| **DataForSEO** | Keyword research, SERP data | Pay-per-use (~$0.50/1000) | From $29/mo | 5000 queries/mo (~$2.50) |
| **SerpAPI** | Google Search results | 100 searches/mo | From $25/mo | 100 searches/mo (free) |
| **Linear** | Task management | 1000 issues/mo | From $8/user/mo | 500 issues/mo (free) |
| **Zernio** | Social media scheduling | Already have API key | - | Unlimited |
| **Tally.so** | Form builder | Free tier | From $29/mo | Free tier |
| **Gamma.app** | Infographic generation | Already have API key | Pro/Ultra | As needed |
| **Neo4j** | Knowledge Graph | Open-source (self-hosted) | - | Self-hosted |
| **OpenDesign** | Design generation | Open-source (self-hosted) | - | Self-hosted |
| **Payload CMS** | Content management | Open-source (self-hosted) | - | Self-hosted |
| **Coolify** | Deployment automation | Open-source (self-hosted) | - | Self-hosted |

**Total Monthly Cost:** ~$2.50 (DataForSEO) + €20 (Hetzner server) = **~$25/month**

### 5.2 Self-Hosted Services

All self-hosted services run on **Hetzner EX44** server (Helsinki):

| Service | Docker Port | Purpose |
|---------|-------------|---------|
| Neo4j | 7474 (HTTP), 7687 (Bolt) | Knowledge Graph database |
| OpenDesign | 3000 | Design-to-code API |
| Payload CMS | 3001 | Content management |
| Coolify | 8000 | Deployment automation |

---

## 6. OpenClaw Configuration

### 6.1 Existing Tools (Already Available)

```json
{
  "tools": {
    "profile": "coding",
    "web": {
      "search": {
        "enabled": true,
        "provider": "grok"
      }
    },
    "skills": [
      "browser-automation",
      "github",
      "canvas"
    ]
  }
}
```

### 6.2 New Tools to Add

```json
{
  "tools": {
    "alsoAllow": [
      "linear-sdk",        // New: Linear task management
      "neo4j-driver",      // New: Knowledge Graph queries
      "dataforseo-client", // New: SEO data API
      "serpapi-client"     // New: SERP analysis
    ]
  }
}
```

### 6.3 Agent Tool Permissions

| Agent | Required Tools |
|-------|---------------|
| PM | `sessions_spawn`, `sessions_send`, `linear_*`, `read`, `write`, `exec` |
| Researcher-A | `exec`, `bash` (DataForSEO Labs via utilities + curl), `read`, `write`, `sessions_send` |
| Writer-A | `read`, `write`, `exec`, `bash` (Neo4j cypher-shell), `sessions_send` |
| Designer-A | `read`, `write`, `exec`, `sessions_send` |
| SEO-A | `exec`, `bash`, `read`, `write`, `sessions_send` |
| Hermes CMS | `exec`, `bash`, `read`, `write`, `sessions_send` |
| Hermes Deploy | `exec`, `bash`, `sessions_send` |

### 6.4 Agent Installation Standard (amended 2026-07-27)

**All pipeline agents are REAL OpenClaw agents** — never Python scripts
masquerading as agents. Standard for every agent (existing and future):

1. **Registration:** entry in `agents.list` of the isolated PM profile
   (`/root/.openclaw-pm/openclaw.json`) — own `workspace`, own `agentDir`
   (`system.md` + `IDENTITY.md`), own sessions + memory. Content symlinked
   into the project repo (same pattern as PM).
2. **Orchestration:** PM spawns agents via `sessions_spawn` (agent-to-agent
   messaging allowlisted via `tools.agentToAgent`). Agents report results to
   PM; PM alone talks to Linear/Telegram.
3. **Independence Rule:** no agent is built on, wraps, or delegates to an
   agent outside the PM profile. No cross-gateway spawning (Milo stays
   fully isolated).
4. **Utilities are NOT agents:** deterministic Python helpers (DataForSEO
   fetch, batch cypher) live in `utilities/` and exist solely as `exec`
   tools agents may call. They have no identity, memory, or agency.
5. **Real data only:** no mock/simulated outputs anywhere; agents fail
   loudly on API errors.
6. **Zero hallucinations:** content agents must ground statistics in Neo4j
   KG facts and self-verify before marking output `verified`.

---

## 7. Workspace Structure

```
/root/dev/agentic-pipeline/
├── docs/
│   ├── architecture-spec.md
│   ├── agents/
│   │   ├── agent-pm.md
│   │   ├── agent-researcher-a.md
│   │   ├── agent-writer-a.md
│   │   ├── agent-designer-a.md
│   │   ├── agent-seo-a.md
│   │   ├── agent-hermes-cms.md
│   │   └── agent-hermes-deploy.md
│   └── integrations/
│       ├── integration-linear.md
│       ├── integration-neo4j.md
│       ├── integration-opendesign.md
│       ├── integration-payload.md
│       └── integration-coolify.md
├── scripts/
│   ├── setup-neo4j.sh
│   ├── setup-opendesign.sh
│   └── setup-payload.sh
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
└── .gitignore
```

---

## 8. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Neo4j Docker container
- [ ] Create Linear project + API keys
- [ ] Build Project Manager agent
- [ ] Test Linear integration (create/update tasks)

### Phase 2: Research + KG (Week 3)
- [ ] Build Researcher agent
- [ ] Integrate DataForSEO API
- [ ] Integrate SerpAPI
- [ ] Test keyword discovery workflow
- [ ] Populate KG with initial facts

### Phase 3: Content Generation (Week 4)
- [ ] Build Writer agent
- [ ] Integrate Neo4j queries
- [ ] Test content generation with fact-grounding
- [ ] Validate zero hallucinations

### Phase 4: Design + OpenDesign (Week 5-6)
- [ ] Install OpenDesign locally
- [ ] Build Designer agent
- [ ] Integrate OpenDesign API
- [ ] Test landing page generation

### Phase 5: SEO + Deployment (Week 7)
- [ ] Build SEO agent
- [ ] Integrate DataForSEO rankings
- [ ] Build Hermes CMS agent
- [ ] Build Hermes Deploy agent
- [ ] Test end-to-end: research → deploy

### Phase 6: Polish + v2 Prep (Week 8-10)
- [ ] Add Zernio social posting
- [ ] Add Gamma.app infographics
- [ ] Optimize agent prompts
- [ ] Document lessons learned
- [ ] Plan Vertical B (WeFab AI) rollout

---

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Hallucinated facts** | High | Medium | Pre-output KG verification, citation requirements |
| **API rate limits** | Medium | Low | Stagger requests, use free tiers wisely |
| **Neo4j performance** | Medium | Low | Index optimization, query caching |
| **Agent coordination failures** | High | Medium | Linear task tracking, timeout monitoring |
| **Deployment failures** | High | Low | Hermes health checks, rollback procedures |
| **Cost overruns** | Low | Low | Budget alerts, free tier prioritization |

---

## 10. Success Criteria

### 10.1 MVP Success (Week 7)

**Functional:**
- ✅ 10 articles published for ProQSmart
- ✅ 5 landing pages live
- ✅ All content fact-grounded (zero hallucinations)
- ✅ Linear shows 100% task completion
- ✅ Core Web Vitals: All green

**Business:**
- ✅ 5+ qualified leads generated
- ✅ Content generation time: <2 hours/week
- ✅ Total cost: <$50/month

### 10.2 v2 Success (Week 10)

**Functional:**
- ✅ Vertical B (WeFab AI) agents deployed
- ✅ 20 articles/month total across both verticals
- ✅ Automated social posting via Zernio
- ✅ Infographics via Gamma.app

**Business:**
- ✅ 20+ qualified leads/month total
- ✅ Content generation time: <1 hour/week
- ✅ Total cost: <$100/month

---

## 11. Maintenance & Operations

### 11.1 Monitoring

**Daily:**
- Check Linear for failed tasks
- Review Neo4j query performance
- Monitor API usage (DataForSEO, SerpAPI)

**Weekly:**
- Review content performance (rankings, traffic)
- Optimize agent prompts based on output quality
- Update KG with new facts/keywords

**Monthly:**
- Cost review (API usage, hosting)
- Agent performance metrics
- Plan next month's content themes

### 11.2 Backup Strategy

**Neo4j:**
- Daily dumps to `/backups/neo4j/`
- Weekly remote backup to Hetzner Object Storage

**Linear:**
- Native Linear backups (cloud)
- Export critical projects monthly

**Workspace Files:**
- Git version control (this repo)
- Daily rsync to backup server

---

## 12. Appendix: Quick Reference

### 12.1 Environment Variables

```bash
# Linear
LINEAR_API_KEY=lin_api_xxx

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# DataForSEO
DATAFORSEO_EMAIL=your-email
DATAFORSEO_PASSWORD=your-password

# SerpAPI
SERPAPI_KEY=your-key

# Zernio
ZERNIO_API_KEY=sk_xxx

# Payload CMS
PAYLOAD_URL=http://localhost:3001
PAYLOAD_EMAIL=admin@payload.com
PAYLOAD_PASSWORD=your-password

# Coolify
COOLIFY_URL=http://localhost:8000
COOLIFY_WEBHOOK_URL=http://localhost:8000/api/webhooks/deploy

# OpenDesign
OPENDESIGN_URL=http://localhost:3000
```

### 12.2 Common Commands

```bash
# Start all services
docker-compose -f docker-compose.yml up -d

# Check Neo4j status
docker exec -it neo4j cypher-shell "MATCH (n) RETURN count(n)"

# Test Linear integration
node scripts/test-linear.js

# Run agent tests
npm test

# Deploy specs to Git
git add . && git commit -m "Update specs" && git push
```

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: Week 4 (after MVP implementation)*

---

## 13. Glossary

### Agent IDs

| Agent ID | Short Name | Role |
|----------|-----------|------|
| `project-manager` | PM | Strategic orchestrator |
| `researcher-vertical-a` | Researcher-A | ProQSmart keyword/trend discovery |
| `writer-vertical-a` | Writer-A | ProQSmart content generation |
| `designer-vertical-a` | Designer-A | ProQSmart UI/UX design |
| `seo-vertical-a` | SEO-A | ProQSmart optimization |
| `hermes-cms-sync` | Hermes CMS | Payload CMS integration |
| `hermes-deploy` | Hermes Deploy | Coolify deployment |
| `researcher-vertical-b` | Researcher-B | WeFab AI keyword/trend discovery (v2) |
| `writer-vertical-b` | Writer-B | WeFab AI content generation (v2) |
| `designer-vertical-b` | Designer-B | WeFab AI UI/UX design (v2) |
| `seo-vertical-b` | SEO-B | WeFab AI optimization (v2) |

### Acronyms

| Acronym | Meaning |
|---------|---------|
| KG | Knowledge Graph |
| CMS | Content Management System |
| SEO | Search Engine Optimization |
| SERP | Search Engine Results Page |
| PM | Project Manager |
| MVP | Minimum Viable Product |
| API | Application Programming Interface |
| SDK | Software Development Kit |

### Task ID Format

Linear task IDs follow the format `MAR-XXX` where:
- `MAR` = Marketing team prefix
- `XXX` = Sequential number (e.g., MAR-123, MAR-124)

**MVP Task Sequence:**
- MAR-123: Project (ProQSmart Content Q3 2026)
- MAR-124: Keyword Research
- MAR-125: Write 10 Articles
- MAR-126: Design 5 Landing Pages
- MAR-127: SEO Optimization
- MAR-128: CMS Sync
- MAR-129: Deploy to Production

### Model Selection Rationale

| Model | Parameters | Use Case | Rationale |
|-------|-----------|----------|-----------|
| `minimax-m3` | ~100B | Reasoning, planning, analysis | Strong reasoning for complex workflows |
| `gemma4:31b` | 31B | Creative writing, content generation | Balanced creativity + fact-grounding |
| `qwen2.5-coder:32b` | 32B | Code generation, technical tasks | Specialized for code output |

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
