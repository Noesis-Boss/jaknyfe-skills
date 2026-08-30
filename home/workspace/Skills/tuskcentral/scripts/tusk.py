#!/usr/bin/env python3
"""
tusk.py — command-line wrapper for tuskcentral.ai.

Send a prompt to any of 30 free/premium models, get the reply back as plain
text. Cookies come from the Clerk session saved by setup.py.

Quick start:
  python3 setup.py                                     # one-time sign-in
  python3 tusk.py --list-models                        # show all models
  python3 tusk.py "Explain CAPE ratio" --model grok   # free Grok 4.3
  python3 tusk.py "Plan Q4 OKRs" --model "Gemini 3.1"  # premium, free sprint
  python3 tusk.py "Write a haiku" --model haiku --new   # fresh chat
  python3 tusk.py "Continue" --chat-id <uuid>          # follow up

By default, replies print to stdout. Use --json for structured output,
--out file.md to save the reply, or --quiet to print nothing (for scripts).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import os
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tusk_lib import TuskClient, TuskSessionMissing, TuskSessionExpired
logger = logging.getLogger(__name__)


def _resolve_model(client: TuskClient, arg: str | None) -> str | None:
    """Accept 'label', 'substring', or a UUID; return the resolved label for display."""
    if not arg:
        return None
    m = client.find_model(arg)
    return m.label


def cmd_list_models(args, client):
    """Show the available Tusk models. The /providers endpoint is unauthenticated."""
    from tusk_lib import fetch_providers, _load_session

    cache = Path("/root/.tuskcentral/models.json")
    if args.refresh or not cache.exists():
        try:
            storage = _load_session()  # optional — pass cookies if we have them
        except Exception:
            storage = None
        models = fetch_providers(storage=storage)
        try:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(
                json.dumps([m.__dict__ for m in models], default=str, indent=2)
            )
        except OSError as e:
            logger.warning("could not write cache: %s", e)
    else:
        try:
            raw = json.loads(cache.read_text())
            from tusk_lib import TuskModel
            models = [TuskModel(**r) for r in raw]
        except Exception as e:
            logger.warning("cache read failed (%s); refreshing", e)
            models = fetch_providers(storage=None)
    if args.json:
        out = [
            {
                "label": m.label,
                "key": m.key,
                "provider": m.provider,
                "is_premium": m.is_premium,
                "options": m.option_keys,
                "tones": m.tone_keys,
                "input_modalities": m.input_modalities,
                "has_web_search": m.has_web_search,
                "has_reasoning": m.has_reasoning,
            }
            for m in models
        ]
        print(json.dumps(out, indent=2))
        return 0
    width = max(len(m.label) for m in models)
    for m in models:
        prem = "💎" if m.is_premium else "🆓"
        opts = "/".join(m.option_keys) if m.option_keys else "-"
        print(f"  {prem} {m.label.ljust(width)}  [{m.provider}]  opts={opts}")
    return 0


def cmd_chat(args, client: TuskClient) -> int:
    if not args.prompt and not sys.stdin.isatty():
        args.prompt = sys.stdin.read().strip()
    if not args.prompt:
        print("error: no prompt provided (give a string or pipe via stdin)", file=sys.stderr)
        return 2

    t0 = time.monotonic()
    try:
        reply = client.chat(
            args.prompt,
            model=args.model,
            model_id=args.model_id,
            option=args.option,
            tone=args.tone,
            web_search=None if args.web_search is None else args.web_search,
            reasoning=None if args.reasoning is None else args.reasoning,
            chat_id=args.chat_id,
            new_chat=args.new,
        )
    except (TuskSessionMissing, TuskSessionExpired) as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    elapsed = time.monotonic() - t0

    if args.json:
        print(json.dumps({
            "model": reply.model,
            "model_id": reply.model_id,
            "chat_id": reply.chat_id,
            "chat_log_id": reply.chat_log_id,
            "text": reply.text,
            "html": reply.html,
            "elapsed_sec": round(elapsed, 2),
            "api_elapsed_sec": round(reply.elapsed_sec, 2),
            "error": reply.error,
        }, indent=2, ensure_ascii=False))
        if reply.error:
            return 4
        return 0

    if not args.quiet:
        header = f"[{reply.model}]  ({elapsed:.1f}s, chat={reply.chat_id})"
        print(header)
        print("-" * len(header))
        if reply.error:
            print(f"⚠️  {reply.error}", file=sys.stderr)
        else:
            print(reply.text or "(empty response)")

    if args.out:
        Path(args.out).write_text(reply.text)
        if not args.quiet:
            print(f"\nSaved to {args.out}", file=sys.stderr)

    return 0 if not reply.error else 4


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tusk",
        description="Talk to tuskcentral.ai from the command line.",
    )
    sub = p.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list-models", help="Show the model catalog.")
    p_list.add_argument("--refresh", action="store_true",
                        help="Re-fetch from the API (default uses cache).")
    p_list.add_argument("--json", action="store_true", help="JSON output.")

    p_chat = sub.add_parser("chat", help="Send a prompt (default if no subcommand).")
    p_chat.add_argument("prompt", nargs="?", help="The prompt text (or pipe via stdin).")
    p_chat.add_argument("--model", help="Model label, substring, or UUID.")
    p_chat.add_argument("--model-id", help="Model UUID (overrides --model).")
    p_chat.add_argument("--option", help="sprint|marathon (default = auto).")
    p_chat.add_argument("--tone", help="technical|creative|work|learn|casual")
    p_chat.add_argument("--web-search", dest="web_search", action=argparse.BooleanOptionalAction,
                         help="Force web search on/off (else follows model default).")
    p_chat.add_argument("--reasoning", dest="reasoning", action=argparse.BooleanOptionalAction,
                         help="Force reasoning on/off (else follows model default).")
    p_chat.add_argument("--chat-id", help="Continue a previous chat by its UUID.")
    p_chat.add_argument("--new", action="store_true", help="Start a fresh chat.")
    p_chat.add_argument("--out", help="Save the reply to this file.")
    p_chat.add_argument("--json", action="store_true", help="JSON output.")
    p_chat.add_argument("--quiet", action="store_true", help="Print nothing on success.")

    p_status = sub.add_parser("status", help="Show session and last chat info.")
    return p


def main() -> int:
    parser = build_parser()
    # If no subcommand and first arg looks like a prompt, default to "chat"
    if len(sys.argv) > 1 and sys.argv[1] not in {"list-models", "chat", "status", "-h", "--help"}:
        argv = ["chat"] + sys.argv[1:]
    else:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        return 0

    try:
        client = TuskClient()
    except TuskSessionMissing as e:
        print(f"error: {e}", file=sys.stderr)
        print("Run: python3 setup.py", file=sys.stderr)
        return 3

    if args.cmd == "list-models":
        return cmd_list_models(args, client)
    if args.cmd == "chat":
        try:
            return cmd_chat(args, client)
        finally:
            client.close()
    if args.cmd == "status":
        from tusk_lib import TUSK_LAST_CHAT_FILE, TUSK_SESSION_FILE
        print(f"Session file: {TUSK_SESSION_FILE}  ({'exists' if TUSK_SESSION_FILE.exists() else 'missing'})")
        print(f"Last chat:    {TUSK_LAST_CHAT_FILE}  ({'exists' if TUSK_LAST_CHAT_FILE.exists() else 'missing'})")
        if TUSK_LAST_CHAT_FILE.exists():
            print(TUSK_LAST_CHAT_FILE.read_text())
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
