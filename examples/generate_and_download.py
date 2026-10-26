"""End-to-end example: submit one generation task, wait, download results.

This is the whole generation flow in ~30 lines. The client polls the task
every few seconds (see `poll_interval`) until PixAI marks it completed.

Run:  python examples/generate_and_download.py "your prompt here" MODEL_ID
      (or edit the constants below)
"""

import sys
from pathlib import Path

from pixai_api import PixAI

TOKEN_FILE = Path.home() / ".pixai_api" / "token.json"
OUTPUT_DIR = "output"


def main() -> int:
    prompt = sys.argv[1] if len(sys.argv) > 1 else "a serene mountain lake at dawn"
    model_id = sys.argv[2] if len(sys.argv) > 2 else "2036163415011877234"

    client = PixAI(token=PixAI.load_token(TOKEN_FILE))

    print(f"[1/3] credits before: {client.quota()}")
    print(f"[2/3] submitting task (model {model_id})...")
    task = client.create_generation_task(
        prompt,
        model_id=model_id,
        width=832,
        height=1216,
        steps=33,
        batch_size=2,
    )
    task_id = task.get("id")
    print(f"      task id: {task_id}")

    def progress(status, _task):
        print(f"[3/3] status: {status}", flush=True)

    final = client.wait_for_task(task_id, timeout=900, on_status=progress)
    urls = PixAI.task_media_urls(final)
    print(f"done — {len(urls)} media file(s):")
    for url in urls:
        print(" ", url)
    for url in urls:
        client.download_file(url, OUTPUT_DIR)
    print(f"credits after: {client.quota()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
