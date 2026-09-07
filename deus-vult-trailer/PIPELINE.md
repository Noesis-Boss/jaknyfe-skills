# DEUS VULT: TEMPLAR WARS — Teaser Assembly Pipeline

## Structure

- `scenes.json` — Scene definitions, timing, transitions, text overlays
- `build.py` — Generates ffmpeg commands from scenes.json
- `assets/sceneNN/` — Place source images/videos here
- `assets/audio/` — Place narration, music, SFX here
- `output/` — Final renders

## Usage

1. Drop source assets into each `assets/sceneNN/` folder:
   - `source.jpg` or `source.mp4` — primary visual
   - `end.jpg` or `end.mp4` — optional end frame for image-to-video
2. Place audio in `assets/audio/`:
   - `narration.wav` — full narration track
   - `music.wav` — orchestral music
   - `sfx/` — individual sound effects
3. Run: `python3 build.py`
4. Output: `output/deus_vult_teaser.mp4`

## Scene Map (16 scenes, 30s total)

| # | Time | Duration | Asset | Transition |
|---|------|----------|-------|------------|
| 01 | 0:00-0:02 | 2.0s | assets/scene01/source | crossfade |
| 02 | 0:02-0:04 | 2.0s | assets/scene02/source | crossfade |
| 03 | 0:04-0:08 | 4.0s | assets/scene03/source | crossfade |
| 04 | 0:08-0:09 | 1.0s | assets/scene04/source | cut |
| 05 | 0:09-0:12 | 3.0s | assets/scene05/source | crossfade |
| 06 | 0:12-0:14 | 2.0s | assets/scene06/source | wipe |
| 07 | 0:14-0:15 | 1.0s | assets/scene07/source | cut |
| 08 | 0:15-0:16 | 1.0s | assets/scene08/source | crossfade |
| 09 | 0:16-0:19 | 3.0s | assets/scene09/source | crossfade |
| 10 | 0:19-0:20 | 1.0s | assets/scene10/source | cut |
| 11 | 0:20-0:22 | 2.0s | assets/scene11/source | crossfade |
| 12 | 0:22-0:25 | 3.0s | assets/scene12/source | wipe |
| 13 | 0:25-0:26 | 1.0s | assets/scene13/source | cut |
| 14 | 0:26-0:28 | 2.0s | assets/scene14/source | crossfade |
| 15 | 0:28-0:29 | 1.0s | assets/scene15/source | crossfade |
| 16 | 0:29-0:30 | 1.0s | assets/scene16/source | fade |
