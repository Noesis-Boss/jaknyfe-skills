# Video Forge architecture

Video Forge is the orchestration layer. Specialist skills own their tool-specific instructions; FFmpeg is a shared media utility rather than the default composition engine.

```text
Brief + constraints
        ↓
Beat sheet / shot plan
        ↓
Asset preparation ─── narration / music / captions
        ↓
Primary production path
  ├─ HyperFrames: HTML/CSS/GSAP compositions
  ├─ Remotion: React/TSX compositions
  ├─ Video Use: source-footage editorial workflow
  ├─ Explainroo: narrated hand-drawn explainers with word-timed scenes
  ├─ Manim: mathematical/explainer animation
  └─ Gemini: targeted generative edit of existing footage
        ↓
FFmpeg finishing (only needed operations)
        ↓
ffprobe + frame/contact-sheet + audio review
        ↓
Approved local deliverable → explicit separate publication approval
```

## Responsibilities

- **Video Forge**: scope, route, sequence stages, preserve constraints, track verification, and report the deliverable.
- **Composition/editing skill**: own timeline/composition semantics and any workflow-specific hard rules.
- **Explainroo** (`Projects/explainroo/`): optional local explainer-video tool; its project instructions own setup and rendering semantics. Video Forge retains brief/plan, provenance, review, and publication boundaries.
- **FFmpeg**: inspect, transform, mux, extract, and finish media in a deterministic local step.
- **Review**: combine machine-readable probe checks with visual and audio inspection; neither alone is sufficient.

## Adding a production capability

Add a specialist only when it provides a distinct production capability or reliable interface. Add its route to `SKILL.md`, define its stage and handoff inputs/outputs here, and avoid copying its full instructions. Keep publishing outside the render pipeline and approval-gated.
