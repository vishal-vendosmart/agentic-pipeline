# MEMORY.md - Long-Term Memory

## Strategic Pivot (August 2026)
- **Shift from SaaS to AI Operations:** Moved away from selling SaaS platforms.
- **The New Offer:** Custom AI agents that handle human-intensive computer operations to deliver end-to-end outcomes.
- **Operational Experience:**
    - **Presence, not a Tool:** Not a dashboard the user operates. The agent lives on a server and has its own chat interface.
    - **Omnichannel Reporting:** Reports and communicates via Teams, Slack, Telegram, and Email (like a true employee).
    - **Tool Integration:** Takes tasks and autonomously updates CRMs, project management tools, and handles documentation.
- **Nuance on "Employees":** We are NOT replacing jobs or human functions (like project management/coordination). We are automating the *computer-based operations* required to reach an outcome.
- **Technical Foundation:**
    - Built on a combination of our internal knowledge graph and the customer's existing/updating knowledge graph.
    - **Data Sovereignty:** Customers own their data; the system is designed so nothing leaves their server.
    - Focus on custom AI agents that operate on the customer's own private data for maximum security and relevance.
- **Full role spec:** `/root/.openclaw/workspace/ROLE.md`
- **Goal:** 10 qualified meetings/month across both brands by end of Q3 2026.
- **Vishal:** Founder, Bengaluru (IST). Phone: +91 9665071506. Server timezone: Asia/Kolkata.
- **Co-founder:** Girish Kadli (ML/AI systems architect). Legal entity: Vendosmart Technologies Pvt Ltd.
- **Brands:** ProQSmart (B2B SaaS procurement) + WeFab AI (AI-native manufacturing).
- **WeFab ICP industries:** Industrial machinery, SPMs, industrial automation & robotics, packaging machinery, material handling / conveyor, process equipment (chemical, pharma, food), energy & battery equipment. **HVAC/climate OUT of ICP**. Mid-market $20M-$500M, 15-50+ years old, 50-500+ engineers, ETO/CTO/MTO.

## Content Lane Pivot (2026-09-22)
- **New lane:** company brain + AI coworkers for mid-market manufacturing. Positioning: build the company brain from decades of static drive data, then build AI coworkers on top that execute workflows per a JD. Humans stop operating SaaS; AI does it better.
- **Voice change:** killed the "shop I visited" opener (reads as fake). Now insight-led from company interactions, focused on the problem the company has.
- **Named companies on HOLD** (use only when Vishal clears): Japanese manufacturers (`japan-icp-targets.md`, incl. StraPack), engineering services companies in India, UAE commercial fitout giant (`GLOBAL_FITOUT_LEADS.md` - ALEC FITOUT, A&T Group, USBC, INC Group).
- **Voice rules for this lane:** `content/voice-rules-company-brain.md` (supersedes pain-first framing).
- **Last post before pivot:** 2026-08-28. 30 posts all-time, all Vishal personal LinkedIn. Top posts: Jul 20 (40.5k impr), Jul 22 (8.8k), Aug 7 (6.3k).

## Automation Platform Split (locked 2026-06-13)

**Windmill** = pure-data scripts (no LLM). **OpenClaw crons** = LLM synthesis.

**Windmill (marketing-stack-v2):** subagent_watchdog (15min), email_check (09:00,21:00 IST), follow_up_anand (11:00 IST), content_poll_v2 (12:00 Helsinki), kg_rebuild_daily (23:55 IST), kg_rebuild_weekly (Sun 02:00 IST).

**OpenClaw crons:** content-notify-a (12h), morning-brief-b (07:00), weekly-retro-d (Sun 20:00), weekly-social-analytics (Wed 18:00), KG Daily/Weekly Rebuild.

**Rule:** Data-only → Windmill. LLM-needed → OpenClaw cron.

## Hard Rules (locked 2026-06-07)
- **Email = Himalaya, ALWAYS.** Config: `/root/.config/himalaya/config.toml`, account `openclaw@proqsmart.com`.
- **SMTP gotcha:** Port 465 BLOCKED. Use 587 + STARTTLS. From: `openclaw@proqsmart.com`, Reply-To: `vishal@proqsmart.com`.
- **Email Permission Rule:** Always ask for permission before sending emails to anyone *except* the following addresses:
    - `vishal@proqsmart.com`
    - `vishal@vendosmart.com`
    - `vishal@wefab.ai`
- **Approval Logic:** An explicit direct command (e.g., "respond to this email") constitutes immediate approval for that specific action.
- **Cron prompts:** Keep under ~600 chars. Script does data work; model formats/sends.
- **Writer is the ONLY path for content (locked 2026-07-28):** Milo does NOT draft content (LinkedIn, blogs, emails). Always: diagnose Writer failure, fix, retry. Voice Rules: `/root/.openclaw/workspace/content/voice-rules-vishal-pain.md`.
- **No unsolicited background work:** No watchdogs, side-quests without explicit ask.
- **Investigate, don't dismiss:** Verify before claiming "false alarm."

## API Verification Rules (added 2026-06-13)
- **NEVER report a count as final without verifying filter params.** Zernio `/v1/posts?status=scheduled`: MUST use `accountId=<_id from /v1/accounts>`. Always fetch accounts list first.
- **Zernio: updating a post is `PUT /posts/{id}`, NOT PATCH.** `PATCH /posts/{id}` returns **405** with an empty body. `PUT` with `{"content": "..."}` returns 200 and preserves `scheduledFor`/`status`. `scripts/zernio/update_thread.mjs` uses PATCH and is broken. (locked 2026-09-23)
- **Never probe a live resource with write methods.** Probing PUT on a real post id overwrote its content. Probe on a throwaway id, or read the spec first. (locked 2026-09-23)

## Tools & APIs
- **Windmill MCP:** In openclaw.json (SSE). Token in `/opt/marketing-stack/dev/workspace/.env.joint`.
- **Zernio API:** `https://zernio.com/api/v1`. Key: `ZERNIO_API_KEY` in `.env.joint`. Client: `scripts/zernio/zernio-api.mjs`.
- **Twenty CRM:** `crm.proqsmart.com` (GraphQL). Creds: `twenty-creds.json`.
- **DataForSEO:** `vishal@proqsmart.com:a25b69e4ad3fbbb2`
- **Himalaya:** `~/.config/himalaya/config.toml`, account `openclaw@proqsmart.com`.

## Model Config (updated 2026-08-01)
- **Primary:** `ollama-cloud/gemma4:31b`. Fallbacks: glm-5.2 → qwen3.5:397b → deepseek-v4-pro → grok-2.
- **kimi-k2.5 was retired 2026-07-31 — removed from all fallback chains.** Do NOT re-add.
- **Subagent model:** gemma4:31b for Writer.
- **Never use grok as default** — all ollama-cloud models are fixed-cost; grok bills per token.
- **Timeout:** 600s (main), 240s (crons needing LLM).
- **Memory/Recall:** Semantic embeddings via local ollama `nomic-embed-text` (768-dim). autoCapture + autoRecall enabled.

## Document & Image Handling
- **Images from Telegram:** Model reads directly (minimax-m3 + grok-4.3 vision-capable).
- **PDF/Word/Excel:** `python3 /root/.openclaw/workspace/scripts/parse_document.py <path>`.

## Browser Automation
- Primary: `openclaw browser` CLI. Profile: `openclaw` (headless). Refs NOT stable across navigations.
- **Pivot rule:** If form-fill fails twice with same error, STOP. Hand to Vishal with screenshot + checklist.

## CRM Best Practices
- Deduplicate before creating: search by email first. Link people to companies. Mark emails as read after processing.

## Content Style
- Paul Graham style (see `SOUL.md`). Direct, no fluff.
- **NEVER em dashes (—) in content.** Hyphens only.
- **NO markdown syntax in social posts** (LinkedIn/X display literally).

## Subagent & Session Rules
- **Subagent failure:** Tell Vishal immediately. Pattern: spawn → wait → check → report + fallback.
- **Session lock:** Never immediately retry failed tool call. Let lock release; retry next message.
- **Writer subagent failure patterns (locked 2026-07-15, REVISED 2026-07-28):**
  1. `bundle-mcp runtime disposed` — set `mcp.sessionIdleTtlMs: 0` (APPLIED).
  2. gateway restart during spawn — watchdog check fixed (APPLIED).
  3. writer too narrow prompt — use `gemma4:31b` primary + fallbacks (APPLIED).
  4. add `write` to writer tools (APPLIED).
- **DO NOT draft content as Milo** — violates role boundary.

## The Verification Protocol (LOCKED 2026-07-29)
1. **Zero Assumption of Success:** Verify state with separate read. Never trust exit code alone.
2. **Close the Loop:** End every request with "Final State Report" — what was requested, evidence of change, "Verified: [Actual State]."
3. **No "Almost Done":** Only report completion when final verification successful.
4. **Failure Accountability:** Admit verification failures immediately.
5. **Audit Trail:** Print "Before" and "After" states for bulk edits.

## Tool Defaults (added 2026-06-14)
- **Default to `browser` tool** for "look at a website and pull data". `web_fetch` is fast but 403s on modern sites, no JS.
- **Use `web_fetch` only for:** simple docs, blogs, public APIs, RSS.
- **Use `browser` for:** tracker sites, e-commerce, social, JS-rendered, login content, 403s on web_fetch.
- **If `web_fetch` 403s → switch to `browser` tool immediately.**

## URL Patterns
- **FlightAware:** `/live/flight/AIC{number}` = LIVE page. `/live/flight/AIC{number}/history/YYYYMMDD` = HISTORY table (different DOM). Use LIVE by default.
- **FlightStats:** `https://www.flightstats.com/v2/flight-tracker/AI/{number}?year=YYYY&month=M&date=D`.

## Sharing Rules
- **Screenshots:** `MEDIA:/path/to/file`.
- **Files/docs:** Paste content inline OR `MEDIA:/root/.openclaw/workspace/filename.md`.
- **Long-form Content (CRITICAL):** For long-form content, strategies, or lengthy reports, do NOT send multiple long messages. Instead: Write the content to a file → add → commit → push to Git → share the public GitHub URL.
- **Git for outlines/strategy docs:** Write → add → commit → push → return GitHub URL.
- **Content Delivery:** For long-form content or lengthy messages (e.g., content drafts, long reports), always put them in an `.md` file and send as an attachment instead of writing them as open messages.

## Key File References
- Role/brand: `ROLE.md`, `SOUL.md`, `CONTEXT.md`
- ICP/leads: `LEADS.md`, `ALL_LEADS.md`
- Content strategy: `linkedin-strategy.md`, `wefab-content-briefs.md`
- Automation: `plans/5-stream-automation-spec.md`
- QRP PRD: `PRD-QRP-Email-System.md`
- Windmill: `windmill/` folder
- Zernio API: `integrations/zernio-api.md`
