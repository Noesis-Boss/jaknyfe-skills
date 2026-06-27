# 7 Prompts from "Claude Designs Like a $10K Agency"

**Video:** [Claude Designs Like a $10K Agency (If You Use These 7 Prompts)](https://www.youtube.com/watch?v=tnlfiR_0XoE)
**Channel:** Hyperautomation Labs
**Extracted:** 2026-06-24

---

## The 7 Prompts

### 1. Show, Don't Tell (Reference → Spec)

> "Don't build anything yet. Just extract the design language and write it back to me as a spec. The color palette as hex codes, the font pairing, the size jumps between headings, the spacing rhythm, the feeling in three words."

**Value to Syndicate:** ★★★★★ — Core technique. Transforms vague aesthetic requests into concrete, reusable design specs. Eliminates the "generic AI look" at the root. Directly applicable to Syndicate's boardroom UI — feed it a reference screenshot (Linear, Stripe, Notion) and extract a spec before building any component. This is the anti-slop prompt.

---

### 2. Tokens Before Components (Design System First)

> "Define the tokens first. A color palette with named roles — background, surface, primary, accent, muted, border. A type scale with a fixed ratio. An eight-point spacing system. Radius and shadow tokens. One single source of truth. Then give it the rule: Every component you build may only use these tokens. No random hex codes, no one-off pixel values."

**Value to Syndicate:** ★★★★★ — This IS the DESIGN.md skill already in the workspace. The video literally describes the exact same concept: named color roles, type scale, spacing system, radius/shadow tokens, strict usage rules. This prompt is the single most important one for Syndicate's UI consistency. Should be baked into every UI generation task.

---

### 3. Name the Aesthetic (Design Movement, Not Adjective)

> Instead of "modern," name an actual design movement. "Editorial, Bauhaus, brutalist, Swiss. Pick the language that fits your brand. And hand Claude the rulebook instead of a vibe. Vague in, vague out. Specific in, stunning out."

**Value to Syndicate:** ★★★★☆ — High leverage for Syndicate's theming. Instead of "make it look good," say "brutalist data dashboard" or "editorial fintech" or "Swiss institutional." Each word carries a known rulebook. This prevents the generic purple-gradient-on-white AI default. Pairs with DESIGN.md — the aesthetic name sets the tone, DESIGN.md encodes the tokens.

---

### 4. Build on Real Foundations (shadcn + Radix + Tailwind)

> "Use shadcn components, wire in my tokens, keep all the styling in Tailwind. shadcn is not a component library you install. It's a collection of beautifully designed component code that you copy straight into your own project. Built on top of Radix, which handles all the accessibility, the keyboard navigation, the focus, the screen reader support for free."

**Value to Syndicate:** ★★★★☆ — Directly actionable. Syndicate already uses Tailwind + shadcn. This prompt is essentially the existing stack. The value is in the phrasing: "wire in my tokens, keep all the styling in Tailwind" — this is the instruction that prevents agents from inventing inline styles or random CSS. Should be standard in every Syndicate UI task.

---

### 5. Never Accept the First Idea (Three Directions)

> "Give me three genuinely distinct directions. Not three color swaps of the same layout. Direction A, bold and editorial. Direction B, calm and premium, lots of white space. Direction C, high energy, saturated, unconventional. Render all three side by side. Take the headline from A, the color from C."

**Value to Syndicate:** ★★★★☆ — This is the creative director pattern. For Syndicate, this means: when building a new view (board, task card, agent dashboard), generate 3 layout variants before committing. Prevents the "first draft is final" trap. Costs one prompt, triples output quality. Especially valuable for the boardroom view and task card modals recently built.

---

### 6. Make It Move with Intention (Motion Design)

> "Use motion. Scroll reveal that fades and lifts elements in by about 16 pixels. A short stagger between items in a group. A custom ease out curve, never linear. Durations between 2 and 500 milliseconds. And respect reduced motion for accessibility. Motion should reward attention, not demand it."

**Value to Syndicate:** ★★★★☆ — Motion is the difference between "demo" and "product." Syndicate's task cards and modals would benefit from: stagger on task lists, fade-in on modal open, subtle hover states on cards. The specific numbers (16px lift, 2-500ms, ease-out) are gold — they prevent the "janky motion" failure mode. Should be standard in the frontend-design workflow.

---

### 7. Close the Loop with Screenshots (Self-Critique)

> "Critique this like a senior art director doing a design review, and be harsh. Is there one clear focal point? Does the hierarchy survive a 3-second squint test? Is anything cramped or floating? Then fix the top three problems and re-render."

**Value to Syndicate:** ★★★★★ — This is the most powerful meta-pattern. The agent renders → screenshots → critiques → fixes → re-renders. This is exactly the verification loop Don already values ("backend green means nothing if the user-facing surface is broken"). For Syndicate, this should be automated: every UI change triggers a screenshot + critique pass before commit. The "3-second squint test" is a concrete, testable quality gate.

---

## Summary: What to Include

| # | Prompt | Action |
|---|--------|--------|
| 1 | Show, Don't Tell | Add as standard pre-build step: extract spec from reference before coding |
| 2 | Tokens Before Components | Already covered by DESIGN.md skill — reinforce in every UI task |
| 3 | Name the Aesthetic | Add to task prompts: "Use [movement] aesthetic" instead of adjectives |
| 4 | Build on Real Foundations | Already standard stack — add explicit "wire tokens, no random hex" rule |
| 5 | Three Directions | Add to major UI tasks: generate 3 variants before committing |
| 6 | Motion with Intention | Add specific motion specs to task prompts (16px, stagger, ease-out, 2-500ms) |
| 7 | Screenshot Critique Loop | Add as mandatory verification step: render → screenshot → critique → fix |

**Top 3 highest-value additions to Syndicate's workflow:**
1. **#7 Screenshot Critique Loop** — automates quality verification, aligns with Don's "verify the surface" principle
2. **#1 Show Don't Tell** — eliminates vague aesthetic requests, produces concrete specs
3. **#5 Three Directions** — prevents first-draft-final syndrome, costs nothing extra
