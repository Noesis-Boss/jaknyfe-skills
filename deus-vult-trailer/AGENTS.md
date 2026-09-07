# Issue Log

## 2026-08-17 — Storyboard trailer rebuild

- Problem: the uploaded storyboard contained timing labels and transition arrows, while the prior crop set omitted the two duel panels.
- Tried: rebuilt the source assets from `/home/.z/chat-uploads/dv_storyboard-9e7414f573d1.png`, tightening crop boundaries and masking the upper-left labels; added both duel scenes to the 30-second sequence.
- Result: rendered `output/deus_vult_teaser.mp4` at 1280×720, 30 fps, exactly 30 seconds. Frame inspection confirmed the timing labels are absent and the sequence includes the logo, battle, cards, council, duels, faction fan, and final title.
