# This $399 Robot Does Tricks — And You Program It

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-02T20:30:02+00:00
- **Video**: https://www.youtube.com/shorts/0CexicXSXW0

## Description

MicroDuck is Hugging Face's newest release — a $399 open-source biped robot you can train yourself with reinforcement learning, and it's playable right out of the box. Program it to do tricks, ride skateboards, or whatever else you can dream up. This is a great look at where AI-powered hardware is heading: cheaper, more accessible, and no longer just for developers. Wild that this is available to buy today.

#MicroDuck #HuggingFace #Robotics #OpenSource #AIHardware

🔗 Product: https://pollen-robotics.com/microduck/

Link to the full video: https://www.youtube.com/watch?v=klqyY5SAQvc

## Transcript

Corey, first story is this. What is this? >> This is Micro Duck. So, this is the newest release from Hugging Face. It's a $399 robot that you can program to do tricks, ride skateboards, like do all kinds of crazy stuff. Bottom line, this is where I think a lot of AI-powered hardware is going. It's becoming a lot cheaper and a lot more accessible to one, the everyday person, and two, the non-developer. So, you can literally go on their website today, buy this Micro Duck for 400 bucks, program it to do whatever you want it to do. It's crazy. >> Unreal that it's available right now. I mean, this is this is I think the future that this stuff is coming out. I'm so excited about it.

## Auto-extracted repos

(none auto-extracted — read the transcript above and identify repo names, then search GitHub)

## Agent eval

**Verdict: hardware story, not a software tool.** The video demos the $399 MicroDuck biped robot (Pollen Robotics / Hugging Face). The OSS repos are real and healthy, but every line of code is gated behind owning the physical robot — no fit for this environment's Bun/TS + Python stack, Zo automations, trading bot, or publishing pipeline.

### pollen-robotics/microduck

Official software stack for the MicroDuck biped robot: firmware and host tooling to program tricks and behaviors. The companion repo `pollen-robotics/microduck_rl` (1,789★, Python, Apache-2.0, pushed 2026-09-05) provides the mjlab RL training environments mentioned in the video.

- **Signals**: 7,460★ · Rust (main) / Python (RL) · Apache-2.0 · pushed 2026-09-03 · not archived
- **Recommendation: SKIP** — hardware-gated; code is useless without buying the $399 robot, and it serves none of this environment's projects (trading bot, KDP publishing, zo.space, automations).

### pollen-robotics/microduck_rl

RL training environments (mjlab) for training MicroDuck policies, per the video's "train yourself with reinforcement learning" pitch.

- **Signals**: 1,789★ · Python · Apache-2.0 · pushed 2026-09-05 · not archived
- **Recommendation: SKIP** — trains policies that only run on MicroDuck hardware; no standalone value for the Python trading-bot/automation stack.
