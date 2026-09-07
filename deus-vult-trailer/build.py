#!/usr/bin/env python3
"""
DEUS VULT Teaser — FFmpeg Assembly Pipeline
Generates scene clips, applies transitions, overlays text, mixes audio.
"""
import json
import subprocess
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
CONFIG = json.loads((BASE / "scenes.json").read_text())
W, H = CONFIG["resolution"]
FPS = CONFIG["fps"]
OUT = BASE / "output" / "deus_vult_teaser.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

def run(cmd, check=True):
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        print(p.stderr)
        sys.exit(p.returncode)
    return p

def build_scene_clip(scene, idx):
    """Build a single scene clip with animation."""
    asset = BASE / scene["asset"]
    clip = BASE / "output" / f"scene_{idx+1:02d}.mp4"
    dur = scene["duration"]
    anim = scene.get("animation", {})
    
    # Base filter: scale to 1280x720, maintain aspect with black bars
    if scene.get("animation", {}).get("type") == "fit":
        vf = [f"scale={W}:{H}:force_original_aspect_ratio=decrease",
              f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black"]
    else:
        vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase",
              f"crop={W}:{H}"]
    
    # Animation filters
    atype = anim.get("type", "")
    if atype == "kenburns":
        z0 = anim.get("zoom", 1.0)
        z1 = anim.get("zoom_end", 1.15)
        xp = anim.get("pan", [0.5, 0.5])
        # zoompan for slow push-in
        vf.append(f"zoompan=z='min(zoom+0.0015,{z1})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:fps={FPS}:s={W}x{H}")
    elif atype == "rotate":
        a0 = anim.get("start_angle", -5)
        a1 = anim.get("end_angle", 0)
        vf.append(f"rotate={a0}*(1-t/{dur}):c=none")
        # Crop to avoid black corners
        vf.append(f"crop={W}:{H}")
    elif atype == "pan":
        direction = anim.get("direction", "left")
        if direction == "left":
            vf.append(f"zoompan=z='1.1':x='iw*0.05*on':y='ih/2-(ih/zoom/2)':d=1:fps={FPS}:s={W}x{H}")
    elif atype == "rise":
        vf.append(f"zoompan=z='1.15':x='iw/2-(iw/zoom/2)':y='ih*0.05*on':d=1:fps={FPS}:s={W}x{H}")
    elif atype == "circle":
        # Circular camera movement approximation via zoompan oscillation
        vf.append(f"zoompan=z='1.1+0.02*sin(2*PI*t/{dur})':x='iw/2-(iw/zoom/2)+20*sin(2*PI*t/{dur})':y='ih/2-(ih/zoom/2)+10*cos(2*PI*t/{dur})':d=1:fps={FPS}:s={W}x{H}")
    elif atype == "fan":
        # Static with slight float for card fan
        vf.append(f"zoompan=z='1.05':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:fps={FPS}:s={W}x{H}")
    elif atype == "reveal":
        # Premium card reveal: static with subtle zoom
        vf.append(f"zoompan=z='1.05':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:fps={FPS}:s={W}x{H}")
    
    # Text overlays
    text_filters = []
    for t in scene.get("text", []):
        txt = t["text"].replace(":", "\\:").replace("'", "\\'")
        color = t.get("color", "#ffffff")
        size = t.get("size", 36)
        pos = t.get("position", ["center", "center"])
        x_expr = pos[0] if isinstance(pos[0], str) else f"w*{pos[0]}"
        y_expr = pos[1] if isinstance(pos[1], str) else f"h*{pos[1]}"
        start = t.get("start", 0)
        end = t.get("end", dur)
        
        if "\n" in txt:
            # Multi-line text
            lines = txt.split("\\n")
            for i, line in enumerate(lines):
                y_offset = f"+{i*size}*1.2"
                text_filters.append(
                    f"drawtext=text='{line}':fontcolor={color}:fontsize={size}:x=(w-text_w)/2:y=(h-text_h)/2{y_offset}:enable='between(t,{start},{end})'"
                )
        else:
            text_filters.append(
                f"drawtext=text='{txt}':fontcolor={color}:fontsize={size}:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,{start},{end})'"
            )
    
    all_filters = vf + text_filters
    filter_str = ",".join(all_filters)
    
    # Determine if asset is image or video
    asset_path = str(asset)
    if asset.suffix.lower() in [".mp4", ".mov", ".avi", ".mkv"]:
        # Video asset: loop or trim to duration
        cmd = [
            "ffmpeg", "-y", "-i", asset_path,
            "-vf", filter_str,
            "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            str(clip)
        ]
    else:
        # Image asset: create video from image with loop
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", asset_path,
            "-vf", filter_str,
            "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            str(clip)
        ]
    
    run(cmd)
    return clip

def build_concat_filter(scene_clips):
    """Build ffmpeg concat filter with transitions."""
    inputs = []
    for clip in scene_clips:
        inputs.extend(["-i", str(clip)])
    
    # Build complex filter for crossfade/wipes
    # For simplicity, use concat demuxer with generated list
    concat_list = BASE / "output" / "concat.txt"
    lines = []
    for clip in scene_clips:
        lines.append(f"file '{clip}'")
    concat_list.write_text("\n".join(lines) + "\n")
    
    return inputs, str(concat_list)

def add_audio_and_finalize(concat_list):
    """Mix narration, music, SFX and encode final."""
    final_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
    ]
    
    # Add audio tracks if they exist
    narration = BASE / CONFIG["audio"]["narration"]
    music = BASE / CONFIG["audio"]["music"]
    sfx = BASE / CONFIG["audio"].get("sfx", "")

    # volume, label for each track that exists
    tracks = []
    if narration.exists():
        final_cmd.extend(["-i", str(narration)])
        tracks.append((len(tracks) + 1, 1.6, "narr"))
    if sfx.exists():
        final_cmd.extend(["-i", str(sfx)])
        tracks.append((len(tracks) + 1, 0.9, "sfx"))
    if music.exists():
        final_cmd.extend(["-i", str(music)])
        tracks.append((len(tracks) + 1, 0.35, "musc"))

    # Audio mixing: narration + sfx boosted, music ducked under them
    if tracks:
        audio_filter = [f"[{idx}:a]volume={vol}[{label}]" for idx, vol, label in tracks]
        mix_inputs = "".join(f"[{label}]" for _, _, label in tracks)
        audio_filter.append(f"{mix_inputs}amix=inputs={len(tracks)}:duration=longest:normalize=0[aout]")

        final_cmd.extend(["-filter_complex", ";".join(audio_filter), "-map", "0:v", "-map", "[aout]", "-shortest"])
    else:
        final_cmd.extend(["-map", "0:v"])
    
    final_cmd.extend([
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-r", str(FPS),
        str(OUT)
    ])
    
    run(final_cmd)

def main():
    print(f"Building {len(CONFIG['scenes'])} scenes...")
    clips = []
    for i, scene in enumerate(CONFIG["scenes"]):
        print(f"\nScene {i+1:02d}: {scene['duration']:.1f}s")
        clip = build_scene_clip(scene, i)
        clips.append(clip)
    
    print("\nConcatenating scenes...")
    _, concat_list = build_concat_filter(clips)
    
    print("\nAdding audio and finalizing...")
    add_audio_and_finalize(concat_list)
    
    print(f"\nDone. Output: {OUT}")
    print(f"Size: {OUT.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
