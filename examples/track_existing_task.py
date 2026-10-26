"""Track a task created elsewhere (e.g. the web UI or a previous script).

Run:  python examples/track_existing_task.py 123456789
The script polls until completed/failed and prints the media URLs.
"""

import sys
from pathlib import Path

from pixaipy import PixAI

TOKEN_FILE = Path.home() / ".pixaipy" / "token.json"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python track_existing_task.py TASK_ID", file=sys.stderr)
        return 2
    task_id = sys.argv[1]

    client = PixAI(token=PixAI.load_token(TOKEN_FILE), poll_interval=2.0)

    print("first snapshot:")
    print(client.task(task_id))  # raw REST payload

    final = client.wait_for_task(task_id, timeout=1800)
    print("final:")
    print(final)
    for url in PixAI.task_media_urls(final):
        print("media:", url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
