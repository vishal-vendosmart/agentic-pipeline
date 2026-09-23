# Brief — WeFab Cost Estimation LinkedIn Series (Vishal's direct context)

## Vendor context (from Vishal, 2026-07-29, verbatim)

WeFab AI is building solutions for historical cost benchmarking from unstructured data — ERP, scanned documents, Excel sheets, etc. Semantic matching, dedup, currency and inflation normalization. Feeding the requirement or BoQ to get prices from historical projects.

Today, all of this is done manually.

The goal is to focus on this problem and stay on the issue that proposal engineering in ETO and MTO industries is a major bottleneck because it decides whether you get the order or not.

The posts need to highlight the pain and time-taking process of estimation which is human-intensive today. The work deals with overwhelming heaps of different files which one has to meticulously go through and verify manually.

## Goal (from Vishal)

Spread awareness that internal cost estimation for proposals and proposal creation itself is a major bottleneck of growth in ETO, MTO industries. Only talk about problem areas. Take readers on a visual journey of the pain. Those who know it should instantly connect. Position Vishal as the thought leader working on this kind of problem.

## Voice — Paul Graham style (per Writer's programming)

- Short sentences. Plain words. Mid-thought openers. No thesis-then-support. One idea per line break. No "this is not X, it is Y" reframe patterns.
- USD throughout. No INR, no lakhs, no crores, no rupees.
- No em dashes (—). Hyphens only.
- No markdown syntax anywhere in post bodies (** __ ` ###).
- No product mention. No WeFab, no AI, no solutions. Pain is the message.
- No HVAC. (Locked ICP exclusion.)
- Role-generic third-person voice. No "we/our/us". Role names: "the estimator", "the proposal engineer", "the design lead", "the founder".
- Founder observation: 1 per week max, mid-post only, never as the opening.
- Every paragraph inside the moment. Time, place, action, artifact. Concrete scenes.

## Series plan — 4 weeks, 4 posts each (16 total)

The Writer decides the structure. Milo has not pre-written the scenes. The Writer is the expert.

Suggested approach (Writer can override):
- 4 weeks × 4 posts × 4 different roles / lenses (cost estimator, proposal engineer, design lead, founder/CEO) — gives a 360° tour of the same bid.
- Or pure 4-pillar rotation (historical hunting / scope ambiguity / time pressure / margin uncertainty) across 4 weeks.
- The Writer should pick whichever structure produces the freshest, most varied scenes.

## Output per week

- One file: `content/wefab-proposal-engineering-week-N.md`
- File starts with `<!-- STANZA:EDIT_MARKER_weekN_v5 -->` as literal first line
- 4 posts, `## Post N` headers, `---` between posts
- 200-350 words per post

## Self-checks (per file)

- `grep -c '—' <file>` = 0
- `head -1 <file>` = marker
- `wc -w <file>` = ~800-1400
- `grep -c '^## Post' <file>` = 4
- `grep -cE '\*\*|__|`' <file>` = 0
- `grep -cE 'INR|lakh|crore|rupee|₹' <file>` = 0

## Final rule

The Writer owns the scenes. Milo only checks against the rules. If a post drifts to generic essay mode, Milo flags it and the Writer rewrites that specific post. Do not pre-write Milo scenes in the brief — the whole point of v5 is to let the Writer write fresh scenes, not re-run Milo's pre-written bones.

## Sequence

Write weeks 1, 2, 3, 4 sequentially. Verify each before moving to the next.