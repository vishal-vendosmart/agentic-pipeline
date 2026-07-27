# Implementation Plan — Agentic Pipeline

**Repository:** https://github.com/vishal-vendosmart/agentic-pipeline  
**Start Date:** 2026-07-26  
**Current Phase:** MVP (Week 3 of 8 — ahead of schedule)

---

## Vision

Build a fully automated agentic pipeline that generates 20+ SEO articles/month across two verticals (ProQSmart + WeFab AI) with <1 hour/week human oversight, zero hallucinations, and <$50/month infrastructure cost.

---

## Phases & Timeline

| Phase | Duration | Success Criteria | Exit Trigger |
|-------|----------|------------------|--------------|
| **MVP** | Week 1-8 | 10 articles published, <2hrs/week, <$50/mo | Week 9 OR metrics met |
| **v2** | Week 9-16 | Vertical B (WeFab AI) live, 20 articles total | Week 17 OR metrics met |
| **v3** | Week 17+ | Full automation, <1hr/week, multi-tenant | Ongoing |

---

## Current Phase Status

**Phase:** MVP
**Week:** 3 of 8 (Days 1-2 complete; Weeks 1-3 goals met ahead of schedule)
**Start Date:** 2026-07-26
**Target End:** 2026-09-20
**Days Remaining:** 54

### Week 1 Goals (2026-07-26 to 2026-08-01) ✅ ALL COMPLETE
- [x] PM agent implementation complete
- [x] Linear integration working (create/update tasks)
- [x] Neo4j Docker container running
- [x] First Linear task created by agent
- [x] v2 Linear project created (prevents MVP stall)

### Week 2 Goals (2026-08-01 to 2026-08-08) ✅ ALL COMPLETE
- [x] Researcher agent implementation
- [x] Neo4j Knowledge Graph schema deployed
- [x] DataForSEO Labs API integration tested (live, $52 balance)
- [x] First keyword research completed (54 keywords in Neo4j)

### Week 3 Goals (2026-08-08 to 2026-08-15) ⚠️ PARTIAL
- [x] Writer agent implementation (real openclaw agent, own gateway)
- [ ] Zernio integration for social posting
- [ ] First 3 articles drafted (1/3 done — 854 words, verified)

### Week 4 Goals (2026-08-15 to 2026-08-22) ❌ NOT STARTED
- [ ] Designer agent implementation (own profile/gateway/heartbeat)
- [ ] OpenDesign + Gamma.app integration
- [ ] First 5 landing pages designed

### Week 5 Goals (2026-08-22 to 2026-08-29) ❌ NOT STARTED
- [ ] SEO agent implementation (own profile/gateway/heartbeat)
- [ ] Content optimization workflow
- [ ] First 3 articles optimized

### Week 6 Goals (2026-08-29 to 2026-09-05) ❌ NOT STARTED
- [ ] Hermes CMS agent implementation (own profile/gateway/heartbeat)
- [ ] Payload CMS integration
- [ ] Content sync workflow tested

### Week 7 Goals (2026-09-05 to 2026-09-12) ❌ NOT STARTED
- [ ] Hermes Deploy agent implementation (own profile/gateway/heartbeat)
- [ ] Coolify deployment automation
- [ ] First article published end-to-end

### Week 8 Goals (2026-09-12 to 2026-09-20) ❌ NOT STARTED
- [ ] Polish + bug fixes
- [ ] Performance optimization
- [ ] Documentation complete
- [ ] MVP metrics validation

---

## Implementation Strategy

### Phase 1: Foundation (Week 1-2)
- PM agent orchestrates everything
- Linear as single source of truth for tasks
- Neo4j KG prevents hallucinations from day one
- **Key:** Build Vertical B infrastructure early (even if agents wait)

### Phase 2: Content Generation (Week 3-4)
- Researcher discovers keywords
- Writer generates fact-grounded content
- Designer creates visuals
- **Key:** All content verified against Neo4j before output

### Phase 3: Optimization + Deployment (Week 5-7)
- SEO agent optimizes content
- Hermes agents sync + deploy
- End-to-end workflow tested
- **Key:** Automate everything, human only reviews

### Phase 4: Polish + Metrics (Week 8)
- Validate MVP success criteria
- Document lessons learned
- Plan v2 evolution
- **Key:** Time-box ends Week 8, v2 starts Week 9 regardless

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **MVP stall** | High | Critical | Time-boxed phases (8 weeks max), weekly v2 tasks |
| **API costs spike** | Medium | High | Daily cost tracking, alerts at $20/mo, free tier优先 |
| **Agent hallucinations** | Low | Critical | Neo4j verification mandatory, zero-trust output |
| **Scope creep** | High | Medium | Strict MVP criteria, v2 tasks in separate project |
| **Motivation decay** | Medium | High | Daily journal, weekly progress reviews, public accountability |
| **Technical debt** | Medium | Medium | Document decisions, refactor Week 8, clean architecture |

---

## MVP Success Metrics

- ✅ **10 articles published** for ProQSmart
- ✅ **5 landing pages live**
- ✅ **<2 hours/week** human time
- ✅ **Zero hallucinations** (Neo4j verified)
- ✅ **<$50/month** total cost
- ✅ **<8 weeks** total time

**If not met by Week 8:** Document why, start v2 anyway, adjust metrics for v2.

---

## v2 Evolution Timeline

| Week | Milestone | Status |
|------|-----------|--------|
| Week 9 | v2 Planning + Vertical B project setup | 📅 Target |
| Week 10 | Vertical B Research agent | 📅 Target |
| Week 11 | Vertical B Writer agent | 📅 Target |
| Week 12 | Vertical B live (10 articles) | 📅 Target |
| Week 13-16 | Optimization + automation | 📅 Target |

---

## Next Milestones

### Immediate (This Week)
- [ ] **Week 1:** PM agent + Linear integration
- [ ] **Week 1:** Create v2 Linear project (prevents MVP stall)
- [ ] **Week 1:** Set up Neo4j Docker container

### Short-term (Next 2 Weeks)
- [ ] **Week 2:** Researcher agent + Neo4j KG
- [ ] **Week 2:** DataForSEO + SerpAPI tested
- [ ] **Week 2:** First keyword research completed

---

## Cost Tracking

| Service | Budget | Current | Status |
|---------|--------|---------|--------|
| DataForSEO | $2.50/mo | $0 | ✅ On track |
| SerpAPI | $0 (free) | $0 | ✅ On track |
| Linear | $0 (free) | $0 | ✅ On track |
| Neo4j | $0 (self-hosted) | $0 | ✅ On track |
| Hetzner | €20/mo | €0 | ✅ On track |
| **Total** | **~$25/mo** | **$0** | **✅ On track** |

**Alert threshold:** $20/month (notify human if exceeded)

---

## Weekly Accountability Check

**Every Friday:**
1. ✅ Log progress toward MVP metrics in IMPLEMENTATION.md
2. ✅ Check if MVP is becoming "too comfortable"
3. ✅ Create at least 1 v2 task in Linear
4. ✅ Update PLAN.md week counter
5. ✅ Review cost tracking

---

**Last Updated:** 2026-07-27
**Version:** 2.0
