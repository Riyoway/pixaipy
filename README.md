# pixaipy

Unofficial, community-made client for the PixAI.art GraphQL/REST API.
Not affiliated with or endorsed by PixAI.

## Status

Verified working against the live API. The API itself is undocumented and
can change at any time; when upstream rotates persisted-query hashes,
requests automatically degrade to inline queries instead of hard-failing.

## Features

- Token-based auth — use your own browser session token
- Optional `login()` — supply a reCAPTCHA token you obtain yourself
- Quota / account summary
- Generation tasks: submit / status / wait / cancel
- Media download from finished tasks
- Generic `graphql()` escape hatch for any documented operation
- API reference in [`docs/API.md`](docs/API.md) — every GraphQL operation
  parsed from the official web bundle, with variable types

## Install

```bash
pip install -e .
```

Python 3.9+ / only dependency is `requests`.

## Authentication

**Recommended:** grab your session token once from your browser.

1. Open pixai.art, log in as usual.
2. In devtools → Network tab, make any request, look at a response header
   named **`Token`** — copy its value.
3. Use token:

```bash
pixai token set eyJhbGciOi...        # stored in ~/.pixaipy/token.json
# or set env var:
export PIXAI_TOKEN=eyJhbGciOi...
```

> Treat the token like a password. It grants full control of **your** account.

**Optional `login()`** — the official login mutation is protected by
reCAPTCHA. Supply a `recaptcha_token` produced by your own browser
session (or by a service you control). The simpler path is token auth
above.

```python
from pixaipy import PixAI
client = PixAI()
client.login("me@example.com", "password", recaptcha_token="<your-token>")
client.save_token()
```

## Quickstart (Python)

```python
import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from pixaipy import PixAI

client = PixAI(token="YOUR_TOKEN")          # or PixAI.load_token based flow

print("credits:", client.quota())           # {"id":..., "quotaAmount": N}

task = client.create_generation_task(
    "portrait of an anime mech in sunset, best quality",
    model_id="2036163415011877234",         # pick an id from YOUR model list
    width=832, height=1216, steps=33,
)
final = client.wait_for_task(task["id"], timeout=600)
for url in PixAI.task_media_urls(final):
    print(url)
    client.download_file(url, "output")
```

## CLI

```bash
pixai quota
pixai generate --prompt "..." --model MODEL_ID --width 832 --height 1216 --wait --out ./out
pixai task 123456789 --wait --out ./out
pixai cancel 123456789
pixai token set|show|clear
```

## API surface

| Method | Description |
| --- | --- |
| `PixAI(token=...)` | Create client |
| `.login(email, pw, recaptcha_token)` | Login (needs a reCAPTCHA token you provide) |
| `.quota()` / `.me()` | Credit balance / account summary |
| `.create_generation_task(prompt, model_id=..., ...)` | Submit generation |
| `.task(id)` | REST status of one task |
| `.wait_for_task(id, timeout=...)` | Poll until done |
| `.cancel_task(id)` | Best-effort cancel |
| `.task_media_urls(task)` | URLs from a completed task |
| `.download_file(url, dir)` | Save media locally |
| `.graphql(query, variables, ...)` | Escape hatch to the full schema |
| `.save_token()/.load_token()` | File helpers |

## Troubleshooting

- **`unauthenticated: ... HTTP 401`** — your token died (PixAI rotates tokens
  server-side; the client refreshes its token automatically from response
  headers — re-export a newer one from the browser if 401s persist).
- **Repeated `HTTP 500`** — PixAI blankets aggressive/blocked traffic in 500s.
  Slow down; the built-in backoff (1s→2s… capped 8s) exists for a reason.
  Sustained storms can result in a temporary block, hours even.
- **`PERSISTED_QUERY_NOT_FOUND`** — hash drift upstream; the library already
  auto-falls-back to an inline query, so you should not normally see this.

## Documentation

Heavy documentation lives in [`docs/API.md`](docs/API.md) — the full
(157-operation) GraphQL catalog parsed from the official web bundle, REST
endpoint list, verified request recipes and the troubleshooting matrix.

Unofficial interoperability tooling. No warranty of availability; respect
PixAI's Terms of Service and rate limits while using it.

## License

MIT — see [LICENSE](LICENSE).
