# Brief: Week 3 — Proposal Engineering Pain Series

## Context
- WeFab AI: AI-native manufacturing marketplace. ICP: ETO/CTO/MTO industrial machinery shops ($20M-$500M, 50-500+ engineers). NOT HVAC.
- Persona rotation: each post speaks to one of {QS, PM, Cost Controller, Procurement Head} via the close shape.
- Voice: Paul Graham. Short sentences. No fluff. Zero em dashes (hyphens only). No markdown syntax.
- See `content/voice-rules-vishal-pain.md` for the full voice doc — READ IT before writing.

## Series arc (already shipped)
- **Week 1** (`wefab-proposal-engineering-week-1.md`): 4 pillars, 4 close-shapes (A/B/C/D). Pillars were: (A) unbudgeted 60% of senior engineers on proposals, (B) perfect-vs-rushed dilemma, (C) wave staffing crisis, (D) translator identity crisis.
- **Week 2** (`wefab-proposal-engineering-week-2.md`): same 4 close-shapes A/B/C/D. Pillars were: (A) stale data ghost, (B) admin friction vs engineering judgment, (C) RFQ inbox void / no ownership, (D) quote-to-kickoff handoff amnesia.

## Week 3 — your job
Write **4 fresh posts** on the SAME 4 pillars but with NEW angles (i.e. the third unique perspective on each pillar). Rotate close-shapes A→B→C→D in order.

### Pillar A (Close Shape A — shared experience)
A new angle on: senior engineers / proposal engineering role / capacity allocation.
Possible angles (pick one, don't repeat week 1 or 2 framing):
- The proposal engineer's KPI problem — they are measured on quote turnaround, not on margin. The metric incentivizes the wrong behavior.
- The "whoever has the Word doc owns the truth" problem.
- The proposal engineer is the only person who sees the full margin picture — and nobody listens.
- The proposal engineer becomes a single point of failure that nobody plans for.

### Pillar B (Close Shape B — quiet observation)
A new angle on: perfect-vs-rushed / proposal quality / timing.
Possible angles:
- The "we'll fix it in execution" lie baked into every rushed quote.
- The cost of being 5% under-quoted is invisible until the project ships.
- The proposal is judged on appearance, not on accuracy — the deck is prettier than the math.
- A 100-page proposal gets 4 minutes of customer attention. The first page matters more than the engineering.

### Pillar C (Close Shape C — open question)
A new angle on: ETO wave staffing / capacity / organizational design.
Possible angles:
- The proposal team scales with revenue, not with quote volume. The wave is invisible to headcount planning.
- Why proposal engineering will never get a dedicated team until the first $5M loss forces it.
- The proposal engineer is the canary in the coal mine for ETO design capacity — but nobody reads the canary.
- The hidden cost of pulling a senior engineer off a $500K project to write a $200K quote.

### Pillar D (Close Shape D — reframing)
A new angle on: identity / translator / role definition.
Possible angles:
- The proposal engineer is the only person who knows the real cost of every product — and the sales team is structurally incentivized not to listen.
- Proposal engineering is sales engineering, not sales — the company should pay for it like engineering, not commission it like sales.
- The proposal engineer is a translator who has to translate three times: customer to engineering, engineering to supply chain, supply chain to commercial.
- Proposal engineering is the only role where you are punished equally for being too slow AND being too cheap. The job is rigged.

## MANDATORY RULES (locked — these are non-negotiable)
1. **STANZA MARKER**: The file MUST start with `<!-- STANZA:EDIT_MARKER_week3_attempt_1 -->` as the very first line. No preamble, no other content before it. This is how I detect you actually wrote/edited the file.
2. **NO em dashes (—) anywhere.** Use hyphens (-) only. Read your draft before saving and confirm zero em dashes.
3. **NO markdown syntax** (`**`, `__`, `` ` ``, `###`) in the post bodies. LinkedIn/X renders them literally. Plain paragraphs only.
4. **Close shapes MUST rotate A→B→C→D.** Do not skip. Do not reorder.
5. **Every post MUST end with a soft, human, conversational close.** Not a CTA. Not a pitch. A reflection or a question that feels earned.
6. **Save to**: `/root/.openclaw/workspace/content/wefab-proposal-engineering-week-3.md`
7. **Length per post**: 200-350 words. Match week 1 + week 2 cadence.
8. **Format per post**: Use `## Post N` (H2) headers, plain paragraphs, `---` between posts. No bullet lists in post bodies.

## After writing
- Verify the file exists at the right path
- Verify the stanza marker is the literal first line
- Grep your own file for em dashes: `grep -c '—' <path>` MUST return 0
- Grep for markdown syntax in post bodies: `grep -E '\*\*|__|`' <path>` should return only matches in the metadata/comments, not in post bodies
- Report back: "Wrote week 3. Marker present. Em dashes: 0. Markdown in bodies: 0."

If any rule fails, FIX IT before reporting done. Do not declare done until every check passes.
