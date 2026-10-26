"""Core client for the unofficial PixAI.art API.

Scope:
  * GraphQL core with Apollo persisted-query + inline-query fallback
  * token-based auth (your own token from the browser, or a login
    helper that accepts a reCAPTCHA token you provide)
  * quota check, generation task submission / status / wait / cancel
  * a generic ``graphql()`` escape hatch so you can call any documented
    query yourself

Use it as you would use the site: on your own account, mind the rate
limits.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import requests

from .errors import PixAIError

log = logging.getLogger(__name__)

# Default request context, mirroring the official web application.
_DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://pixai.art",
    "Referer": "https://pixai.art/",
}


class PixAI:
    """Small, conservative client for the unofficial PixAI API."""

    API_URL = "https://api.pixai.art/graphql"
    REST_HOST = "https://api.pixai.art"

    # Verified persisted-query hash for createGenerationTask. If PixAI rotates
    # hashes, the inline-query auto-fallback keeps calls working.
    HASH_CREATE_GENERATION_TASK = (
        "61b5dafa7ade64f847051cdca7024b359bae652421834b8f78423d7640f17d96"
    )

    _APOLLO_EXT = {"clientLibrary": {"name": "@apollo/client", "version": "4.1.3"}}

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        timeout: tuple = (5.0, 30.0),
        max_retries: int = 2,
        poll_interval: float = 2.5,
        user_agent: Optional[str] = None,
    ):
        """
        Args:
            token: Your session token. Grab it once from your browser's
                devtools (the ``Token`` response header PixAI sets at login)
                or call :meth:`login`. Never share a token.
            timeout: (connect, read) seconds per HTTP request.
            max_retries: Extra attempts on 5xx / connection errors, with an
                exponential 1s, 2s... backoff. Keep this small: PixAI answers
                sustained request storms with temporary blanket HTTP 500s.
            poll_interval: Seconds between task-status polls.
            user_agent: Override the default browser-like User-Agent.
        """
        self.token = token
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self.poll_interval = poll_interval
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": user_agent or self._default_user_agent()}
        )

    # ------------------------------------------------------------------ auth

    @staticmethod
    def _default_user_agent() -> str:
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )

    def login(self, email: str, password: str, recaptcha_token: str) -> str:
        """Log in with your own account and capture the session token.

        The official login mutation is protected by reCAPTCHA, so a
        ``recaptcha_token`` produced by your own browser session is
        required. The simpler everyday path is token auth:

        >>> client = PixAI(token="paste-token-from-devtools")

        Raises:
            PixAIError: if ``recaptcha_token`` is missing or the login fails.
        """
        if not recaptcha_token:
            raise PixAIError(
                "Login requires a reCAPTCHA token from your own browser "
                "session. Alternatively pass an existing session token: "
                "PixAI(token=...)."
            )
        payload = {
            "query": (
                "mutation login($input: RegisterOrLoginInput!) { "
                "login(input: $input) { id email emailVerified } }"
            ),
            "variables": {
                "input": {
                    "email": email,
                    "password": password,
                    "recaptchaToken": recaptcha_token,
                }
            },
        }
        response = self._request(
            "POST", self.API_URL, json=payload, include_token=False
        )
        self.token = response.headers.get("Token")
        if not self.token:
            raise PixAIError("Login failed: no Token header in the response")
        log.info("Logged in; token captured from response header")
        return self.token

    # Token file helpers (plaintext JSON — protect the file yourself).

    def save_token(self, path: Union[str, Path] = "token.json") -> Path:
        """Persist the current token to ``{"token": "..."}`` JSON."""
        if not self.token:
            raise PixAIError("No token to save")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"token": self.token}, indent=1), encoding="utf-8"
        )
        return path

    @classmethod
    def load_token(cls, path: Union[str, Path] = "token.json") -> str:
        """Read a token previously written by :meth:`save_token`."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        token = (data or {}).get("token")
        if not token:
            raise PixAIError(f"No token found in {path}")
        return token

    # -------------------------------------------------------------- plumbing

    def _headers(self, include_token: bool = True) -> Dict[str, str]:
        headers = dict(_DEFAULT_HEADERS)
        if include_token and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """HTTP with exponential backoff on 5xx/connection errors.

        PixAI rate-limits aggressive traffic by blanketing it in HTTP 500s;
        the backoff here is deliberately gentle so normal use stays healthy.
        """
        last_exc: Optional[Exception] = None
        for attempt in range(1 + self.max_retries):
            if attempt:
                time.sleep(min(1 * (2 ** (attempt - 1)), 8))
            try:
                response = self.session.request(
                    method, url, timeout=self.timeout, **kwargs
                )
                if 500 <= response.status_code < 600:
                    log.warning(
                        "Server error %s (%d/%d)",
                        response.status_code,
                        attempt + 1,
                        self.max_retries + 1,
                    )
                    continue
                # PixAI may silently rotate your token on any call.
                new_token = response.headers.get("Token")
                if new_token:
                    self.token = new_token
                return response
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                log.warning("Connection error (%d): %s", attempt + 1, exc)
        if last_exc:
            raise last_exc
        raise PixAIError("Max retries exceeded")

    def _graphql_raw(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST", self.API_URL, json=payload, headers=self._headers()
        )
        try:
            return response.json()
        except ValueError as exc:
            raise PixAIError(f"Non-JSON response from GraphQL: {exc}") from exc

    def graphql(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        persisted_hash: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Call any GraphQL operation against the PixAI schema.

        Escape hatch so the library stays tiny while the schema large.
        Provide ``persisted_hash`` when you know a verified APQ hash for the
        operation; the server also accepts plain inline queries.

        Returns the raw GraphQL response dict (check ``"errors"`` yourself).
        """
        payload: Dict[str, Any] = {"query": query, "variables": variables or {}}
        if operation_name:
            payload["operationName"] = operation_name
        if persisted_hash:
            payload["extensions"] = {
                **self._APOLLO_EXT,
                "persistedQuery": {"version": 1, "sha256Hash": persisted_hash},
            }
        return self._graphql_raw(payload)

    def _graphql_inline(
        self,
        query: str,
        variables: Dict[str, Any],
        operation_name: Optional[str] = None,
        persisted_hash: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Inline-first call with automatic APQ fallback.

        Try the persisted hash (matches the official web app). When the
        server answers ``PERSISTED_QUERY_NOT_FOUND`` (hash drift), resend as
        a plain inline query — PixAI accepts those.
        """
        if persisted_hash:
            payload: Dict[str, Any] = {
                "variables": variables,
                "extensions": {
                    **self._APOLLO_EXT,
                    "persistedQuery": {"version": 1, "sha256Hash": persisted_hash},
                },
            }
            if operation_name:
                payload["operationName"] = operation_name
            result = self._graphql_raw(payload)
            for err in result.get("errors", []) or []:
                code = (err.get("extensions") or {}).get("code", "")
                if code == "PERSISTED_QUERY_NOT_FOUND":
                    log.warning("Hash drift on %r; falling back to inline query", operation_name)
                    result = self._graphql_raw(
                        {"query": query, "variables": variables}
                    )
                    break
            return result
        return self._graphql_raw({"query": query, "variables": variables})

    # ----------------------------------------------------------------- quota

    def me(self) -> Dict[str, Any]:
        """Current account summary (id, email, quotaAmount...)."""
        result = self._graphql_inline(
            "query getMyQuota { me { id email quotaAmount } }", {}
        )
        if "errors" in result:
            raise PixAIError(f"me() failed: {result['errors']}")
        data = (result.get("data") or {}).get("me")
        if data is None:
            raise PixAIError("me() returned no data (token invalid?)")
        return data

    def quota(self) -> int:
        """Current credit balance (raises if the token is dead)."""
        data = self.me()
        return int(data.get("quotaAmount") or 0)

    # ------------------------------------------------------------ generation

    def create_generation_task(
        self,
        prompt: str,
        *,
        model_id: str,
        negative_prompts: str = "",
        width: int = 1280,
        height: int = 768,
        steps: int = 33,
        cfg_scale: float = 5,
        sampler: str = "Euler a",
        clip_skip: int = 2,
        batch_size: int = 4,
        seed: Union[int, str] = "",
        lora: Optional[Dict[str, Any]] = None,
        extra_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Submit an image generation task and return the task object.

        This mirrors the parameters the official web UI submits (verified
        against the live API). ``model_id`` is required — pick one from your
        account's model list (e.g. the "Anime V4" family on pixai.art).

        Returns the created task dict (``id``, ``status``...), NOT the
        images; poll with :meth:`task` / :meth:`wait_for_task`.
        """
        if not prompt:
            raise PixAIError("prompt is required")
        if not model_id:
            raise PixAIError("model_id is required (see your PixAI model list)")

        parameters: Dict[str, Any] = {
            "prompts": prompt,
            "extra": {"naturalPrompts": prompt},
            "priority": 1000,
            "width": width,
            "height": height,
            "modelId": str(model_id),
            "negativePrompts": negative_prompts,
            "samplingSteps": steps,
            "samplingMethod": sampler,
            "cfgScale": cfg_scale,
            "seed": seed,
            "clipSkip": clip_skip,
            "batchSize": batch_size,
            "enableADetailer": True,
            "controlNets": [],
            "lightning": False,
            "promptHelper": {
                "withStage": False,
                "userWantToEnable": False,
                "enable": False,
            },
        }
        if lora:
            parameters["lora"] = lora
        if extra_parameters:
            parameters.update(extra_parameters)

        inline_query = (
            "mutation createGenerationTask($parameters: JSONObject!) { "
            "createGenerationTask(parameters: $parameters) { ...TaskBase } } "
            "fragment TaskBase on Task { id userId parameters outputs artworkId "
            "artworkIds artworks { createdAt hidePrompts id isNsfw isSensitive "
            "mediaId title updatedAt } status priority runnerId startedAt "
            "createdAt updatedAt media { id type width height urls { variant url } } "
            "type { type model } retryCount }"
        )
        result = self._graphql_inline(
            inline_query,
            {"parameters": parameters},
            operation_name="createGenerationTask",
            persisted_hash=self.HASH_CREATE_GENERATION_TASK,
        )
        if "errors" in result:
            raise PixAIError(f"create_generation_task failed: {result['errors']}")
        return (result.get("data") or {}).get("createGenerationTask") or {}

    def task(self, task_id: str) -> Dict[str, Any]:
        """Fetch one generation task via REST (``/v1/task/{id}``).

        Raises:
            PixAIError: on 401/403 (dead token) so callers can re-auth.
        """
        url = f"{self.REST_HOST}/v1/task/{task_id}"
        response = self._request("GET", url, headers=self._headers())
        if response.status_code in (401, 403):
            raise PixAIError(f"unauthenticated: task fetch returned HTTP {response.status_code}")
        if response.status_code >= 400:
            raise PixAIError(f"task fetch failed: HTTP {response.status_code}")
        return response.json()

    def wait_for_task(
        self,
        task_id: str,
        *,
        timeout: float = 900,
        interval: Optional[float] = None,
        on_status: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """Poll a task until it completes; returns the final task object.

        Args:
            timeout: give up after this many seconds.
            interval: override ``poll_interval``.
            on_status: progress callback ``(status_string, task_dict)``.
        """
        interval = float(interval if interval is not None else self.poll_interval)
        deadline = time.monotonic() + timeout
        status = ""
        while True:
            task = self.task(task_id)
            status = str((task or {}).get("status") or "")
            log.debug("Task %s status=%s", task_id, status)
            if on_status:
                on_status(status, task)
            if status == "completed":
                return task
            if status == "failed":
                raise PixAIError(
                    f"generation task {task_id} failed: "
                    f"{task.get('failureReason') or task}"
                )
            if time.monotonic() >= deadline:
                raise PixAIError(
                    f"timeout waiting for task {task_id} (last status={status!r})"
                )
            time.sleep(interval)

    @staticmethod
    def task_media_urls(task: Dict[str, Any]) -> List[str]:
        """Extract image URLs from a completed task (REST ``outputs.mediaUrls``)."""
        outputs = task.get("outputs") or {}
        if not isinstance(outputs, dict):
            return []
        urls = outputs.get("mediaUrls") or []
        return [u for u in urls if isinstance(u, str) and u]

    def cancel_task(self, task_id: str) -> bool:
        """Best-effort cancel of a queued generation task (unofficial mutation).

        PixAI's cancel mutation has no published persisted hash — the inline
        query is sent instead, and spelling drift upstream may break it.
        """
        payload = {
            "operationName": "cancelTask",
            "variables": {"taskId": str(task_id)},
            "query": "mutation cancelTask($taskId: ID!) { cancelTask(taskId: $taskId) { id status } }",
            "extensions": self._APOLLO_EXT,
        }
        result = self._graphql_raw(payload)
        if "errors" not in result:
            return True
        log.warning("cancel_task failed: %s", result["errors"])
        return False

    # -------------------------------------------------------------- download

    def download_file(
        self,
        url: str,
        output_dir: Union[str, Path] = ".",
        filename: Optional[str] = None,
    ) -> Optional[Path]:
        """Download one media URL into ``output_dir``; returns the path."""
        try:
            response = self.session.get(url, timeout=(10, 120))
            response.raise_for_status()
        except requests.RequestException as exc:
            log.error("Download failed for %s: %s", url, exc)
            return None
        if not url.lower().split("?")[0].endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4")):
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/") and not content_type.startswith("video/"):
                log.error("URL did not return media content-type (%s)", content_type)
                return None
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        if not filename:
            stem = Path(url.split("?")[0]).stem or "pixai"
            ext = Path(url.split("?")[0]).suffix or ".png"
            filename = f"{stem[:40]}{ext}"
        out = directory / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(response.content)
        log.info("Saved: %s (%d bytes)", out, len(response.content))
        return out
