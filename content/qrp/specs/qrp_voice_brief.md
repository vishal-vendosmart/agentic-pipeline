# QRP Voice Brief — Reference for Content Sub-Agent

**Audience for this brief:** Milo-Content sub-agent. Read this before writing any QRP post.
**Owner:** Vishal Patil, founder WeFab AI / ProQSmart
**Channel:** LinkedIn primary, X secondary (cross-post of anchor)
**Cadence:** 3 posts/week LinkedIn, 1 thread/week X
**Window:** 8-week build to establish "QRP" as a category Vishal coined

---

## The Term

**QRP = Quote Ready Package.** A package a vendor can quote from without 6 emails of clarification. Coined by Vishal after years of watching B2B sourcing fail on incomplete RFQs. Not a new idea. A name for an old pain.

**Pronoun:** "A QRP" (singular), "QRPs" (plural), "this is QRP" / "this is non-QRP" (adjective).

**Anti-patterns:**
- Do NOT say "I made up a word." QRP is a working term Vishal has used for a while. It's a label, not an invention.
- Do NOT call it "the new way" or "the future of sourcing" in the same breath as defining it. Earn that line over 6+ posts.
- Do NOT pitch WeFab in the first 6 posts. The term has to land as Vishal's idea, not as a product feature.

---

## The Pain Frame

The single most important metaphor: **"sitting on a rocking horse."**

Sourcing feels like work. It's motion without movement. The buyer sends 8 RFQs, gets 8 prices for 8 different things, picks the lowest, and wonders why the parts show up wrong.

**The 60-hour chase** is the canonical example. 47 custom parts. 8 vendors. 4 different materials assumed. 6 different tolerances. 0 parts ordered. $400 over estimate. Felt productive. Was a rocking horse.

**The 8-quotes problem** is the second anchor. Same RFQ → 8 different prices → buyer picks the lowest → that vendor quoted the cheapest assumption → parts arrive wrong → "we quoted to the spec you sent."

---

## Voice Rules (Paul Graham)

**Mechanics:**
- First person. "I", "we", "I watched", "I saw."
- Short sentences. Short paragraphs. One idea per beat.
- No em dashes (—). Hyphens (-) only.
- No markdown in social content. LinkedIn and X show markdown literally. No `**`, no `#`, no `>`, no bullet markdown.
- Lists are allowed when written as plain text lines (just hyphens, not markdown bullets).
- No "synergize", "leverage", "optimize", "ecosystem", "stakeholder."
- No "I would argue" / "It is important to note" / "In today's fast-paced world."
- No emojis. (Vishal's existing LinkedIn voice uses zero.)

**Opening hooks (pick one pattern, never re-use same hook twice in a row):**
- Specific scene: "I watched a $2M automation line ship 8 months late."
- Personal confession: "I spent 60 hours last year chasing 8 vendors."
- Direct contradiction: "Your RFQ is not an RFQ. It's a guess."
- Number first: "8 quotes. 8 different parts. 1 buyer confused."

**Closer (one of these patterns):**
- Specific memory prompt: "What's the worst 'please quote' you've ever sent or received?"
- Yes/no: "Have you ever been burned by the cheapest quote?"
- Reframe: "You weren't burned by the vendor. You were burned by your own RFQ."

**Length:** 600-900 chars for short, 1000-1400 for long-form. Never Twitter-length on LinkedIn.

**Visual cues:**
- Line breaks between every idea. 1-3 sentences per paragraph max.
- White space is the rhythm. The reader should feel a beat between thoughts.

---

## The 12-Post Arc (Locked)

**Phase 1 — Define (Weeks 1-2):**
1. Define QRP. (Anchor post, already drafted in qrp_content_anchors.md, needs V2)
2. The rocking horse — 60-hour chase, Monday-Friday breakdown.
3. 8 quotes, 8 different things — the cheapest vendor is almost always wrong.
4. Why everyone sends a bad RFQ — empathize, then introduce the fix.
5. The QRP score — 0-100 across 5 categories.
6. Most expensive word in RFQs is "standard" — short, sharp.

**Phase 2 — Make it personal (Weeks 3-4):**
7. What a QRP gets you — 48-hour response, comparable quotes.
8. The 5 things every QRP must have — drawings, specs, BOM, acceptance, logistics.
9. Templates are not the answer — contrarian, templates make RFQs worse.
10. A QRP is a love letter to your vendors — reframe vendor relationship.
11. The 5 questions every vendor will ask — preempt them in the RFQ.
12. The buyer who shows up with a QRP wins every time — closing prophecy.

**Phase 3 — Anchor to WeFab (Weeks 5-6, posts 13-18):** Soft WeFab tie-ins, case studies, the rfq@wefab.ai mechanism. The audience knows the term by now. WeFab is the natural answer.

---

## Handoff Convention

- Sub-agent writes drafts to: `/root/.openclaw/workspace/qrp_drafts/post_NN_slug.md`
- Each draft file MUST start with:
  ```
  # Post N — [Working Title]
  Status: DRAFT v1
  Target length: 600-900 / 1000-1400 chars
  Hook: [first 2 lines as they'd appear in LinkedIn]
  Working notes: [where the sub-agent thinks this post sits in the arc]
  ```
- Sub-agent never schedules to Zernio.
- Sub-agent never creates images. Sub-agent can suggest visuals in a "## Visual suggestion" section.
- Sub-agent never edits an existing post without explicit ask. Always writes new draft.
- After writing, sub-agent reports: file path, char count, hook line, any open questions for Vishal.

## What "Done" Looks Like

A draft is done when:
- It follows voice rules above
- Hook lands in first 2 lines
- One idea per beat, white space preserved
- Ends with a specific memory prompt, not "thoughts?"
- No em dashes, no markdown syntax, no buzzwords
- Mentions WeFab only if post is in Phase 3
- Sub-agent can defend the choice of every paragraph

If the sub-agent can't defend a line, it cuts it.
