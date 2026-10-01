---
name: add-motion
description: Add, review, or tune purposeful motion in an existing web or app interface. Use when asked to add animation, improve interaction feedback, refine transitions, or audit a named interface area for motion. Pair with frontend-design only when the same request also needs visual direction or broader UI styling; consult design-md and project DESIGN.md for persistent design tokens.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Add Motion

Add motion to clarify a state change, preserve spatial context, confirm an action, or create deliberate emphasis. Skip motion when it adds no useful information. Never scan or animate an entire interface unless the user explicitly asks for that scope.

## Before editing

1. Identify the exact component, interaction, and outcome requested. For an audit, report candidate changes first; implement only if implementation is requested or clearly included.
2. Read the project README and AGENTS guidance. For frontend work, find and follow the nearest `DESIGN.md` literally. Inspect current interaction states and reuse existing tokens, libraries, and conventions.
3. Keep behavior intact: keyboard access, focus order, task completion, state semantics, and reduced-motion usability must not depend on animation. Ask only if a product choice changes the control's meaning or available action.
4. Choose the smallest implementation that fits the stack. Prefer CSS transitions for simple UI state changes; use the existing animation library when orchestration, gestures, or shared-layout motion require it. Do not add a dependency for a small transition.

## Coordinate with visual design

Use `frontend-design` alongside this skill only when the request includes both visual design work and motion. Let `frontend-design` guide the overall visual direction and component styling; use this skill for motion purpose, timing, implementation, accessibility, and motion verification. For a motion-only request, stay here. Read `design-md` or the project's `DESIGN.md` when design tokens or established visual rules apply. Do not invoke either skill as a reason to expand the requested scope.

## Design the motion

For each proposed animation, state its purpose and trigger. Match motion to the relationship between states:

- Keep persistent elements visually continuous when their position or size changes.
- Make overlays and menus feel connected to their trigger; use a centered origin for modal dialogs.
- Animate opening and closing as a pair. Give hover, keyboard focus, and pressed states equivalent feedback.
- Keep frequent actions quick and restrained. Reserve longer or more expressive motion for rare, intentional moments.
- Preserve immediate feedback and completion. Motion must not block clicks, keyboard input, focus, or access to newly shown content.

Prefer `transform` and `opacity` for movement. Animate colors only when useful. Avoid `transition: all`; name the properties. Avoid animating layout dimensions or positional properties in routine interactions. If a measured layout transition is necessary, keep it local and check its cost at the target viewport. Avoid persistent `will-change` and unnecessary animation loops.

Use project tokens when present. Otherwise, treat these as starting ranges, not mandatory values: 100–180 ms for press or hover feedback; 150–250 ms for small anchored surfaces; 200–350 ms for dialogs and drawers. Shorten motion as travel distance and interaction frequency decrease. Choose easing that responds promptly and settles cleanly. Retargetable transitions are usually better than restarting keyframe sequences for interactive state changes.

## Accessibility and device behavior

Honor `prefers-reduced-motion` for the specific motion introduced. Remove large travel, parallax, and nonessential looping; preserve the state change and use an immediate change or restrained fade where useful. Do not apply blanket overrides to every element or remove essential user-triggered feedback indiscriminately.

Do not rely on hover alone. Keep touch and keyboard operation usable. Gate hover-only movement to hover-capable fine pointers when the framework does not already do this. During direct manipulation, track the pointer without easing; settle after release.

## Implement and verify

1. Make the smallest scoped change. Avoid unrelated visual cleanup or behavior changes.
2. Inspect the diff for unintended selectors, `transition: all`, expensive animated properties, duplicate animation libraries, and missing reduced-motion treatment.
3. Run the relevant project check if one exists and the task warrants it. Open the affected screen in a browser at desktop and narrow widths; exercise the actual trigger, close/reversal, keyboard focus, and reduced-motion mode. Check for clipping, layout shifts, blocked controls, or motion that obscures content.
4. For a user-visible enhancement, capture and inspect a screenshot of the rendered result before calling it complete. If browser verification is unavailable, report the specific limitation and do not claim visual completion.
5. Summarize the changed interaction and the verification evidence. Record a durable project decision in its project log only when it changes project guidance or is significant project work.
