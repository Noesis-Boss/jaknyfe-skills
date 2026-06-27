#!/usr/bin/env python3
"""
Headroom A/B harness — runs (slot, headline) samples through control and headroom
arms, scores the output, and writes a Markdown report.

Usage:
  bun run scripts/run_ab.py --input sample-input/sample.json [--arms control headroom] [--n 1] [--model gpt-4o-mini] [--max-cost 0.50]

Token counting is done with tiktoken (cl100k_base — close enough for both arms;
the harness reports both raw char count and tiktoken count so deltas are honest).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import urllib.request
import urllib.error

# Lazy-loaded so the harness still imports without tiktoken installed
try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except ImportError:  # pragma: no cover
    _ENC = None

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from score import score_tweet  # noqa: E402

ArmName = Literal["control", "headroom"]

SYSTEM_PROMPT = (
    "You are @zdsentry. Write a single X/Twitter post (<= 280 chars) reacting to "
    "the headline. Sharp, opinionated, conservative-libertarian lean. 1-2 hashtags. "
    "No emojis. No em-dash chains. No AI vocabulary (delve, pivotal, underscore, "
    "landscape, tapestry, etc). End with 'Follow me for more...'. Reply with ONLY "
    "the tweet text."
)

HEADROOM_PROXY_URL = os.environ.get("HEADROOM_PROXY_URL", "http://localhost:8787")
DEFAULT_MODEL = os.environ.get("EVAL_MODEL", "gpt-4o-mini")

# Per-million-token prices (USD) — only gpt-4o-mini by default; adjust via env
PRICE_PER_MTOK = {
    "gpt-4o-mini": {"in": 0.15, "out": 0.60},
    "gpt-4o":      {"in": 2.50, "out": 10.00},
    "claude-3-5-sonnet-20241022": {"in": 3.00, "out": 15.00},
}


@dataclass
class Sample:
    slot: str
    headline: str
    context_chunks: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "Sample":
        return cls(
            slot=d["slot"],
            headline=d["headline"],
            context_chunks=d.get("context_chunks", []),
        )


@dataclass
class ArmResult:
    arm: ArmName
    sample_index: int
    slot: str
    headline: str
    input_tokens: int
    input_chars: int
    output_tokens: int
    output_chars: int
    cost_usd: float
    tweet: str
    quality_score: int
    error: str | None = None
    duration_s: float = 0.0


def build_user_prompt(sample: Sample) -> str:
    parts = [f"Headline: {sample.headline}"]
    if sample.context_chunks:
        parts.append("Context:")
        for i, c in enumerate(sample.context_chunks, 1):
            parts.append(f"[{i}] {c}")
    return "\n\n".join(parts)


def count_tokens(text: str) -> tuple[int, int]:
    if _ENC is None:
        return len(text) // 4, len(text)  # rough fallback
    return len(_ENC.encode(text)), len(text)


def call_openai_compatible(
    *,
    base_url: str,
    api_key: str | None,
    model: str,
    system: str,
    user: str,
) -> tuple[str, int, int, float]:
    """
    Hits an OpenAI-compatible /v1/chat/completions endpoint. Returns
    (text, input_tokens, output_tokens, cost_usd).
    """
    import urllib.request, json

    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ZO_API_KEY")
    if not api_key:
        raise RuntimeError("No API key: set OPENAI_API_KEY or pass api_key")

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    duration = time.time() - t0

    text = data["choices"][0]["message"]["content"].strip()
    usage = data.get("usage", {})
    in_tok = usage.get("prompt_tokens", 0)
    out_tok = usage.get("completion_tokens", 0)

    pricing = PRICE_PER_MTOK.get(model, PRICE_PER_MTOK["gpt-4o-mini"])
    cost = (in_tok * pricing["in"] + out_tok * pricing["out"]) / 1_000_000
    return text, in_tok, out_tok, cost


def run_arm(
    arm: ArmName,
    sample: Sample,
    idx: int,
    *,
    model: str,
    api_key: str | None,
) -> ArmResult:
    user = build_user_prompt(sample)
    in_tok_pre, in_chars = count_tokens(user)
    base_url = "https://api.openai.com"
    error = None
    duration = 0.0

    if arm == "headroom":
        # Sanity-check proxy before paying for the call
        try:
            with urllib.request.urlopen(f"{HEADROOM_PROXY_URL}/health", timeout=2) as r:
                if r.status != 200:
                    raise RuntimeError(f"headroom proxy unhealthy at {HEADROOM_PROXY_URL}")
        except (urllib.error.URLError, ConnectionError) as e:
            raise RuntimeError(
                f"headroom proxy unreachable at {HEADROOM_PROXY_URL}: {e}. "
                "Start it with `headroom serve --port 8787` or pass --arm control only."
            ) from e
        base_url = HEADROOM_PROXY_URL

    try:
        t0 = time.time()
        text, in_tok_reported, out_tok, cost = call_openai_compatible(
            base_url=base_url,
            api_key=api_key,
            model=model,
            system=SYSTEM_PROMPT,
            user=user,
        )
        duration = time.time() - t0
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        return ArmResult(
            arm=arm,
            sample_index=idx,
            slot=sample.slot,
            headline=sample.headline,
            input_tokens=in_tok_pre,
            input_chars=in_chars,
            output_tokens=0,
            output_chars=0,
            cost_usd=0.0,
            tweet="",
            quality_score=0,
            error=error,
            duration_s=duration,
        )

    in_tok = in_tok_reported or in_tok_pre
    out_chars = len(text)
    return ArmResult(
        arm=arm,
        sample_index=idx,
        slot=sample.slot,
        headline=sample.headline,
        input_tokens=in_tok,
        input_chars=in_chars,
        output_tokens=out_tok,
        output_chars=out_chars,
        cost_usd=cost,
        tweet=text,
        quality_score=score_tweet(text),
        duration_s=duration,
    )


def aggregate(results: list[ArmResult]) -> dict:
    by_arm: dict[str, list[ArmResult]] = {}
    for r in results:
        by_arm.setdefault(r.arm, []).append(r)
    out = {}
    for arm, items in by_arm.items():
        ok = [r for r in items if r.error is None]
        out[arm] = {
            "n": len(items),
            "errors": sum(1 for r in items if r.error),
            "input_tokens_total": sum(r.input_tokens for r in items),
            "output_tokens_total": sum(r.output_tokens for r in items),
            "cost_total": round(sum(r.cost_usd for r in items), 6),
            "quality_avg": round(sum(r.quality_score for r in ok) / max(len(ok), 1), 1),
            "duration_s_total": round(sum(r.duration_s for r in items), 2),
        }
    return out


def write_report(results: list[ArmResult], agg: dict, model: str, out_path: Path) -> None:
    lines = []
    lines.append(f"# Headroom A/B report")
    lines.append("")
    lines.append(f"- **When**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- **Model**: `{model}`")
    lines.append(f"- **Samples**: {len({r.sample_index for r in results})}")
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| Arm | n | errors | input tok (sum) | output tok (sum) | $ total | quality avg |")
    lines.append("|---|---|---|---|---|---|---|")
    for arm, a in agg.items():
        lines.append(
            f"| {arm} | {a['n']} | {a['errors']} | {a['input_tokens_total']} | "
            f"{a['output_tokens_total']} | ${a['cost_total']:.4f} | {a['quality_avg']} |"
        )
    if "headroom" in agg and "control" in agg:
        c = agg["control"]
        h = agg["headroom"]
        if c["input_tokens_total"] > 0:
            tok_delta = (h["input_tokens_total"] - c["input_tokens_total"]) / c["input_tokens_total"] * 100
            cost_delta = (h["cost_total"] - c["cost_total"]) / max(c["cost_total"], 1e-9) * 100
            qual_delta = h["quality_avg"] - c["quality_avg"]
            lines.append("")
            lines.append("## Delta (headroom vs control)")
            lines.append("")
            lines.append(f"- Input tokens: **{tok_delta:+.1f}%**")
            lines.append(f"- Cost: **{cost_delta:+.1f}%**")
            lines.append(f"- Quality: **{qual_delta:+.1f} pts**")
            lines.append("")
            if tok_delta <= -20 and qual_delta >= -5 and h["errors"] == 0:
                lines.append("**Decision: PASS** — headroom meets promotion criteria.")
            else:
                lines.append("**Decision: HOLD** — headroom does not yet meet promotion criteria.")
    lines.append("")
    lines.append("## Per-sample")
    lines.append("")
    for r in results:
        status = "❌" if r.error else "✅"
        lines.append(f"### {status} Sample {r.sample_index} — {r.arm} — {r.slot}")
        lines.append("")
        lines.append(f"- Headline: {r.headline}")
        lines.append(
            f"- Input: {r.input_tokens} tok / {r.input_chars} chars | "
            f"Output: {r.output_tokens} tok / {r.output_chars} chars | "
            f"${r.cost_usd:.5f} | quality {r.quality_score}/100 | {r.duration_s:.2f}s"
        )
        if r.error:
            lines.append(f"- **Error**: {r.error}")
        else:
            lines.append("")
            lines.append("> " + (r.tweet or "").replace("\n", "\n> "))
        lines.append("")
    out_path.write_text("\n".join(lines))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--arms", nargs="+", default=["control"], choices=["control", "headroom"])
    p.add_argument("--n", type=int, default=1, help="Repeat each sample N times")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-cost", type=float, default=None, help="Skip if estimated cost exceeds")
    p.add_argument("--api-key", default=None)
    p.add_argument("--out-dir", type=Path, default=REPO_ROOT / "reports")
    args = p.parse_args()

    raw = json.loads(args.input.read_text())
    samples = [Sample.from_dict(s) for s in (raw if isinstance(raw, list) else [raw])]
    if not samples:
        print("no samples in input", file=sys.stderr)
        return 2

    est_calls = len(samples) * len(args.arms) * args.n
    if args.max_cost is not None and est_calls * 0.001 > args.max_cost:
        print(f"estimated cost ${est_calls*0.001:.4f} > cap ${args.max_cost}, refusing", file=sys.stderr)
        return 3

    results: list[ArmResult] = []
    for i in range(args.n):
        for s in samples:
            for arm in args.arms:
                r = run_arm(arm, s, idx=len({x.sample_index for x in results}), model=args.model, api_key=args.api_key)
                results.append(r)
                flag = "❌" if r.error else "✅"
                print(f"{flag} {r.arm} sample={r.sample_index} slot={r.slot} q={r.quality_score} ${r.cost_usd:.4f}", flush=True)

    agg = aggregate(results)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = args.out_dir / f"ab-{stamp}.md"
    write_report(results, agg, args.model, out)
    print(f"\nReport: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
