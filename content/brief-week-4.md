# Brief: Week 4 — Proposal Engineering Pain Series (FINAL)

## Context
- WeFab AI: AI-native manufacturing marketplace. ICP: ETO/CTO/MTO industrial machinery shops ($20M-$500M, 50-500+ engineers). NOT HVAC.
- Persona rotation: each post speaks to one of {QS, PM, Cost Controller, Procurement Head} via the close shape.
- Voice: Paul Graham. Short sentences. No fluff. Zero em dashes (hyphens only). No markdown syntax.
- See `content/voice-rules-vishal-pain.md` for the full voice doc — READ IT before writing.

## Series arc (already shipped — DO NOT REPEAT)
- **Week 1** (`wefab-proposal-engineering-week-1.md`): Pillars were (A) unbudgeted 60% of senior engineers on proposals, (B) perfect-vs-rushed dilemma, (C) wave staffing crisis, (D) translator identity crisis.
- **Week 2** (`wefab-proposal-engineering-week-2.md`): Pillars were (A) stale data ghost, (B) admin friction vs engineering judgment, (C) RFQ inbox void / no ownership, (D) quote-to-kickoff handoff amnesia.
- **Week 3** (`wefab-proposal-engineering-week-3.md`): Pillars were (A) speed-vs-accuracy KPI misalignment, (B) "we'll fix it in execution" lie, (C) hidden cost of pulling senior engineers off paying projects, (D) sales incentive vs margin trap.

## Week 4 — your job
Write **4 fresh posts** on the SAME 4 pillars but with the FOURTH unique angle per pillar (final pass). Rotate close-shapes A→B→C→D in order. This is the closing arc — give it weight.

### Pillar A (Close Shape A — shared experience)
A new angle on: senior engineers / proposal engineering role / capacity allocation. (The fourth perspective.)
Possible angles:
- The proposal engineer never gets a performance review because no one is their manager.
- Senior engineers get promoted to proposal engineering as a "reward" — and stop doing the work they were promoted for.
- The proposal engineer is the only person in the company who knows what the shop can actually build — and they are the lowest paid person who knows it.
- The proposal engineer's calendar is owned by everyone, so it is owned by no one.

### Pillar B (Close Shape B — quiet observation)
A new angle on: proposal quality / timing / accuracy economics.
Possible angles:
- The proposal gets reviewed by the customer more carefully than by the company that wrote it.
- The most expensive line item in a proposal is the one nobody questioned.
- Every "rush job" proposal is a small future project that the company is volunteering to lose money on.
- The proposal engineer's confidence on the bid day is inversely correlated with the margin they'll actually earn.

### Pillar C (Close Shape C — open question)
A new angle on: organizational design / capacity / wave response.
Possible angles:
- If proposal engineering is so critical, why is it never the first role a growing ETO hires? Why is it always the fifth?
- What does it say about a company when its most strategic function is run by whoever happens to be free on Tuesday?
- The proposal function gets funded after the first crisis — never before. Why does the lesson always cost money?
- If we removed proposal engineering from the senior engineer pool tomorrow, what would actually break first — and how fast?

### Pillar D (Close Shape D — reframing)
A new angle on: identity / translator / role definition.
Possible angles:
- Proposal engineering isn't a role. It's the absence of a system. The role exists because the company hasn't built the workflow that would replace it.
- The proposal engineer is not a person — it's a missing product in the company's tech stack. The person is a workaround for the missing software.
- Calling it "proposal engineering" hides what it really is: the most expensive admin function in the company, dressed up in technical language.
- The proposal engineer is the only person in the company who has to be good at sales, engineering, supply chain, AND project management — and is paid as if they are doing only one of those.

## MANDATORY RULES (locked — these are non-negotiable)
1. **STANZA MARKER**: The file MUST start with `<!-- STANZA:EDIT_MARKER_week4_attempt_1 -->` as the very first line. No preamble, no other content before it. This is how I detect you actually wrote/edited the file.
2. **NO em dashes (—) anywhere.** Use hyphens (-) only. Read your draft before saving and confirm zero em dashes.
3. **NO markdown syntax** (`**`, `__`, `` ` ``, `###`) in the post bodies. LinkedIn/X renders them literally. Plain paragraphs only.
4. **Close shapes MUST rotate A→B→C→D.** Do not skip. Do not reorder.
5. **Every post MUST end with a soft, human, conversational close.** Not a CTA. Not a pitch. A reflection or a question that feels earned. This is the FINAL week — make the closes land.
6. **Save to**: `/root/.openclaw/workspace/content/wefab-proposal-engineering-week-4.md`
7. **Length per post**: 200-350 words. Match weeks 1-3 cadence.
8. **Format per post**: Use `## Post N` (H2) headers, plain paragraphs, `---` between posts. No bullet lists in post bodies.

## After writing
- Verify the file exists at the right path
- Verify the stanza marker is the literal first line
- Grep your own file for em dashes: `grep -c '—' <path>` MUST return 0
- Grep for markdown syntax in post bodies: `grep -E '\*\*|__|`' <path>` should return only matches in the metadata/comments, not in post bodies
- Report back: "Wrote week 4. Marker present. Em dashes: 0. Markdown in bodies: 0."

If any rule fails, FIX IT before reporting done. Do not declare done until every check passes.