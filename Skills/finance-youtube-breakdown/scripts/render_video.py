#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(args):
    result = subprocess.run(args, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "FFmpeg failed")


def main():
    parser = argparse.ArgumentParser(description="Render an approval-gated finance YouTube draft from a manifest.")
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text())
    scenes = manifest["scenes"]
    output = Path(manifest.get("output", manifest_path.parent / "draft" / "draft.mp4")).resolve()
    narration = Path(manifest["narration"]).resolve() if manifest.get("narration") else None
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="finance-video-") as temp:
        temp_path = Path(temp)
        clips = []
        for index, scene in enumerate(scenes):
            image = Path(scene["image"]).resolve() if scene.get("image") else None
            video = Path(scene["video"]).resolve() if scene.get("video") else None
            audio = Path(scene["audio"]).resolve()
            clip = temp_path / f"scene-{index:03d}.mp4"
            duration = float(scene.get("duration", 0))
            if duration <= 0:
                probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(audio)], text=True, capture_output=True, check=True)
                duration = float(probe.stdout.strip())
            motion = scene.get("motion")
            vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=yuv420p"
            if video:
                video_args = ["-stream_loop", "-1"]
                if scene.get("video_start"):
                    video_args += ["-ss", str(scene["video_start"])]
                video_args += ["-i", str(video)]
                run(["ffmpeg", "-y", *video_args, "-i", str(audio), "-t", f"{duration:.3f}", "-vf", vf, "-r", "30", "-c:v", "libx264", "-preset", "ultrafast", "-threads", "2", "-c:a", "aac", "-shortest", str(clip)])
                clips.append(clip)
                continue
            if motion == "ken-burns":
                direction = 1 if index % 2 == 0 else -1
                vf = f"scale=2112:1188,zoompan=z='min(1+0.035*on/({duration:.3f}*30),1.035)':x='iw/2-(iw/zoom/2)+{direction}*(iw/zoom-iw)/2':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,format=yuv420p"
            run(["ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", str(image), "-i", str(audio), "-t", f"{duration:.3f}", "-vf", vf, "-r", "30", "-c:v", "libx264", "-preset", "ultrafast", "-threads", "2", "-c:a", "aac", "-shortest", str(clip)])
            clips.append(clip)
        silent = temp_path / "silent.mp4"
        transition = 0.65
        inputs = [arg for clip in clips for arg in ("-i", str(clip))]
        video_parts = [f"[{i}:v]" for i in range(len(clips))]
        audio_parts = [f"[{i}:a]" for i in range(len(clips))]
        video_chain = video_parts[0]
        elapsed = float(scenes[0].get("duration", 0))
        for i in range(1, len(clips)):
            video_out = f"v{i}"
            video_chain = f"{video_chain}[{i}:v]xfade=transition=fade:duration={transition}:offset={elapsed - transition:.3f}[{video_out}]"
            elapsed += float(scenes[i].get("duration", 0)) - transition
            video_chain = f"{video_chain};[{video_out}]"
        audio_duration = elapsed
        audio_chain = "".join(audio_parts) + f"concat=n={len(audio_parts)}:v=0:a=1,atrim=duration={audio_duration:.3f},asetpts=N/SR/TB[a]"
        filter_complex = ";".join([video_chain + "format=yuv420p[v]", audio_chain])
        run(["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-threads", "2", "-c:a", "aac", str(silent)])
        inputs = ["-i", str(silent)]
        if narration:
            inputs += ["-i", str(narration)]
        filters = []
        if manifest.get("captions"):
            captions = Path(manifest["captions"]).resolve()
            filters.append(f"subtitles={captions}")
        if filters:
            command = ["ffmpeg", "-y", *inputs, "-vf", ",".join(filters), "-map", "0:v", "-map", "1:a" if narration else "0:a", "-t", f"{elapsed:.3f}", "-c:v", "libx264", "-c:a", "aac", str(output)]
            run(command)
        else:
            if narration:
                run(["ffmpeg", "-y", *inputs, "-map", "0:v", "-map", "1:a", "-t", f"{elapsed:.3f}", "-c:v", "copy", "-c:a", "aac", str(output)])
            else:
                shutil.copy2(silent, output)
    print(output)


if __name__ == "__main__":
    main()
