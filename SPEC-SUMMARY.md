# Specification Summary — Agentic Pipeline

**Status:** ✅ All specs complete
**Created:** 2026-07-26
**Last Updated:** 2026-07-27

---

## ✅ Completed Specifications (17 documents)

### Agent Specs (7)
1. **PM Agent** — `docs/agents/agent-pm.md` — orchestrator, Linear task bus, A2A
2. **Researcher-A** — `docs/agents/agent-researcher-a.md` — live DataForSEO + Neo4j
3. **Writer-A** — `docs/agents/agent-writer-a.md` — SEO drafts from domain knowledge
4. **Designer-A** — `docs/agents/agent-designer-a.md` — React/Tailwind, OpenDesign + Gamma (not built)
5. **SEO-A** — `docs/agents/agent-seo-a.md` — content + technical SEO (not built)
6. **Hermes CMS** — `docs/agents/agent-hermes-cms.md` — Payload CMS sync (not built)
7. **Hermes Deploy** — `docs/agents/agent-hermes-deploy.md` — Coolify deployment (not built)

### Integration Specs (9)
1. **Linear** — `docs/integrations/integration-linear.md`
2. **Neo4j** — `docs/integrations/integration-neo4j.md`
3. **DataForSEO** — `docs/integrations/integration-dataforseo.md`
4. **SerpAPI/SerpBear** — `docs/integrations/integration-serpapi.md`
5. **OpenDesign** — `docs/integrations/integration-opendesign.md`
6. **Payload CMS** — `docs/integrations/integration-payload.md`
7. **Coolify** — `docs/integrations/integration-coolify.md`
8. **Gamma** — `docs/integrations/integration-gamma.md`
9. **Zernio** — `docs/integrations/integration-zernio.md`

### Architecture + Meta (1)
1. **Architecture** — `docs/architecture-spec.md` (includes §6.4 Agent Installation Standard)

---

## Agent Installation Status

| Agent | Status | Gateway | Profile |
|-------|--------|---------|---------|
| pm-agent | ✅ Live | :18790 | ~/.openclaw-pm |
| researcher-a | ✅ Live | :18793 | ~/.openclaw-researcher-a |
| writer-a | ✅ Live | :18794 | ~/.openclaw-writer-a |
| designer-a | ❌ Not built | — | — |
| seo-a | ❌ Not built | — | — |
| hermes-cms | ❌ Not built | — | — |
| hermes-deploy | ❌ Not built | — | — |

**Standard:** All agents are real OpenClaw agents with own profile/gateway/heartbeat (see architecture-spec §6.4).
**Coordination:** A2A (cross-gateway `openclaw agent`) + Linear task bus (labeled issues + heartbeat polling).
