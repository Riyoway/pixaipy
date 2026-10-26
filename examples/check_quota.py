"""Check the credit balance of a PixAI account via the unofficial API.

Run:  python examples/check_quota.py  (token from ~/.pixai_api/token.json)
or:   PIXAI_TOKEN=... python examples/check_quota.py <token>
"""

import os
import sys
from pathlib import Path

from pixai_api import PixAI, PixAIError

TOKEN_FILE = Path.home() / ".pixai_api" / "token.json"


def main() -> int:
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    elif os.environ.get("PIXAI_TOKEN"):
        token = os.environ["PIXAI_TOKEN"]
    elif TOKEN_FILE.exists():
        token = PixAI.load_token(TOKEN_FILE)
    if not token:
        print("No token. Run `pixai token set <TOKEN>` first.", file=sys.stderr)
        return 1

    client = PixAI(token=token)
    info = client.me()
    print(f"Account id : {info.get('id')}")
    print(f"Email      : {info.get('email')}")
    print(f"Credits    : {info.get('quotaAmount')}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PixAIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
