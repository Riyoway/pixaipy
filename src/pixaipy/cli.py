"""Command line interface for pixaipy.

    pixai token set <TOKEN>
    pixai quota
    pixai generate --prompt "..." --model MODEL_ID [--out DIR] [--wait]
    pixai task TASK_ID [--wait]
    pixai cancel TASK_ID
"""

import argparse
import json
import os
import sys
from pathlib import Path

from .client import PixAI
from .errors import PixAIError

DEFAULT_TOKEN_FILE = Path.home() / ".pixaipy" / "token.json"


def _load_token(args) -> str:
    if getattr(args, "token", None):
        return args.token
    env = os.environ.get("PIXAI_TOKEN")
    if env:
        return env
    path = Path(args.token_file)
    if path.exists():
        return PixAI.load_token(path)
    raise PixAIError(
        f"No token. Run `pixai token set <TOKEN>` or set PIXAI_TOKEN "
        f"(token file expected at {path})."
    )


def _client(args) -> PixAI:
    return PixAI(token=_load_token(args), timeout=args.timeout)


def cmd_token(args) -> int:
    path = Path(args.token_file)
    if args.token_command == "set":
        if not args.value:
            print("usage: pixai token set <TOKEN>", file=sys.stderr)
            return 2
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"token": args.value.strip()}, indent=1), encoding="utf-8")
        print(f"Token saved to {path} (plaintext — protect this file)")
        return 0
    if args.token_command == "show":
        token = _load_token(args)
        print(token[:8] + "..." + token[-4:])
        return 0
    if args.token_command == "clear":
        if path.exists():
            path.unlink()
            print(f"Removed {path}")
        return 0
    return 2


def cmd_quota(args) -> int:
    info = _client(args).me()
    print(json.dumps(info, ensure_ascii=False, indent=1))
    return 0


def _print_progress(status: str, _task) -> None:
    print(f"  status: {status}", flush=True)


def cmd_generate(args) -> int:
    client = _client(args)
    task = client.create_generation_task(
        args.prompt,
        model_id=args.model,
        negative_prompts=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        batch_size=args.batch,
        cfg_scale=args.cfg,
        sampler=args.sampler,
        clip_skip=args.clip_skip,
    )
    task_id = task.get("id") or task.get("taskId")
    print(f"Task created: {task_id}")
    if not args.wait:
        print("Poll with: pixai task", task_id)
        return 0
    final = client.wait_for_task(task_id, timeout=args.timeout_wait, on_status=_print_progress)
    urls = PixAI.task_media_urls(final)
    print(f"Completed — {len(urls)} media file(s):")
    for u in urls:
        print(" ", u)
        if args.out:
            client.download_file(u, args.out)
    return 0


def cmd_task(args) -> int:
    client = _client(args)
    if args.wait:
        final = client.wait_for_task(args.task_id, timeout=args.timeout_wait, on_status=_print_progress)
        urls = PixAI.task_media_urls(final)
        print("Completed — media URLs:")
        for u in urls:
            print(" ", u)
        if args.out:
            for u in urls:
                client.download_file(u, args.out)
    else:
        print(json.dumps(client.task(args.task_id), ensure_ascii=False, indent=1))
    return 0


def cmd_cancel(args) -> int:
    ok = _client(args).cancel_task(args.task_id)
    print("cancelled" if ok else "cancel failed (task may be running/finished)")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pixai", description="Unofficial PixAI.art API command line"
    )
    parser.add_argument("--token", help="use this token instead of the token file")
    parser.add_argument("--token-file", default=str(DEFAULT_TOKEN_FILE))
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="per-request read timeout in seconds")
    sub = parser.add_subparsers(dest="command", required=True)

    p_token = sub.add_parser("token", help="manage the stored session token")
    p_token.add_argument("token_command", choices=["set", "show", "clear"])
    p_token.add_argument("value", nargs="?", help="token for the 'set' command")
    p_token.set_defaults(func=cmd_token)

    p_quota = sub.add_parser("quota", help="show account summary and credit balance")
    p_quota.set_defaults(func=cmd_quota)

    p_gen = sub.add_parser("generate", help="submit an image generation task")
    p_gen.add_argument("--prompt", required=True)
    p_gen.add_argument("--model", required=True, help="model ID from your PixAI model list")
    p_gen.add_argument("-n", "--negative", default="")
    p_gen.add_argument("-W", "--width", type=int, default=1280)
    p_gen.add_argument("-H", "--height", type=int, default=768)
    p_gen.add_argument("--steps", type=int, default=33)
    p_gen.add_argument("--cfg", type=float, default=5)
    p_gen.add_argument("--sampler", default="Euler a")
    p_gen.add_argument("--batch", type=int, default=4)
    p_gen.add_argument("--clip-skip", type=int, default=2)
    p_gen.add_argument("--wait", action="store_true", help="poll until finished")
    p_gen.add_argument("--timeout-wait", type=float, default=900)
    p_gen.add_argument("--out", help="download finished media to this directory")
    p_gen.set_defaults(func=cmd_generate)

    p_task = sub.add_parser("task", help="inspect one generation task")
    p_task.add_argument("task_id")
    p_task.add_argument("--wait", action="store_true")
    p_task.add_argument("--timeout-wait", type=float, default=900)
    p_task.add_argument("--out", help="download finished media to this directory")
    p_task.set_defaults(func=cmd_task)

    p_cancel = sub.add_parser("cancel", help="best-effort cancel of a queued task")
    p_cancel.add_argument("task_id")
    p_cancel.set_defaults(func=cmd_cancel)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args) or 0
    except PixAIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
