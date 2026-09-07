# DEUS VULT: TEMPLAR WARS — Cinematic Teaser Pipeline

FFmpeg assembly pipeline for a 30-second 1280×720 30fps cinematic trailer.

## Structure

```
deus-vult-trailer/
├── build.py              # Main assembly script
├── scenes.json           # Scene definitions (timing, animation, text)
├── README.md             # This file
├── assets/
│   ├── scene01/          # Noesis Games emblem
│   ├── scene02/          # Noesis Games presents
│   ├── scene03/          # Saracen cavalry charge
│   ├── scene04/          # Saracen card back
│   ├── scene05/          # Saladin commander card
│   ├── scene06/          # Hospitaller fortress
│   ├── scene07/          # Hospitaller card back
│   ├── scene08/          # Falk de Villaret card
│   ├── scene09/          # French royal council
│   ├── scene10/          # French Crown card back
│   ├── scene11/          # Philip IV commander card
│   ├── scene12/          # Templars march
│   ├── scene13/          # Templar card back
│   ├── scene14/          # Jacques de Molay card
│   ├── scene15/          # Legendary Factions fan
│   ├── scene16/          # Final table + DEUS VULT logo
│   ├── audio/            # narration.mp3, music.mp3, sfx/
│   └── output/           # Generated clips + final video
└── output/
    ├── scene_01.mp4      # Per-scene clips
    ├── ...
    ├── scene_16.mp4
    ├── concat.txt
    └── deus_vult_teaser.mp4  # Final output
```

## Quick Start

```bash
cd /home/workspace/deus-vult-trailer

# 1. Drop source images into each scene folder
#    Supported: .jpg, .jpeg, .png, .mp4, .mov
#    Name them: source.jpg (or source.mp4 for video clips)

# 2. (Optional) Add audio
#    assets/audio/narration.mp3
#    assets/audio/music.mp3

# 3. Build
python3 build.py
```

## Scene Configuration

Edit `scenes.json` to adjust:
- `duration` — clip length in seconds
- `asset` — path to source image/video (relative to project root)
- `animation.type` — `kenburns`, `rotate`, `pan`, `rise`, `reveal`, `fan`
- `animation.zoom`, `zoom_end`, `pan`, `direction`
- `transition.type` — `crossfade`, `wipe`, `dissolve`
- `text[]` — overlay text with timing, color, size, position

## Supported Animations

| Type | Effect |
|------|--------|
| `kenburns` | Slow push-in zoom |
| `rotate` | Tilt rotation |
| `pan` | Horizontal tracking |
| `rise` | Vertical rise |
| `reveal` | Subtle zoom for card reveals |
| `fan` | Gentle float for card backs |

## Text Overlays

```json
{
  "text": "YOUR TEXT",
  "color": "#d4af37",
  "size": 48,
  "position": ["center", "center"],
  "start": 0.5,
  "end": 1.8
}
```

## Audio

Place files in `assets/audio/`:
- `narration.mp3` — voiceover (ducked under music)
- `music.mp3` — orchestral score

The pipeline mixes narration + music automatically if both exist.

## Output Specs

- Resolution: 1280×720
- Frame rate: 30fps
- Codec: H.264 (libx264) CRF 18
- Audio: AAC 192k
- Total duration: 30 seconds

## Notes

- Text must exactly match storyboard. The pipeline preserves exact strings.
- Card flips are simulated via zoom/rotate filters. For true 3D card flips, replace the image asset with a pre-flipped sequence or video clip.
- Scene 15 (Legendary Factions fan) expects a single image with all four card backs arranged for the fan reveal, or replace with a video clip.
- Audio sync requires narration and music to be pre-timed to the 30-second timeline.
