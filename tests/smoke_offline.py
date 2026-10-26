"""Offline smoke tests — no network, requests is stubbed.

Run:  python tests/smoke_offline.py
Covers:
  1) quota()/me() parsing
  2) PERSISTED_QUERY_NOT_FOUND -> automatic inline-query fallback
  3) wait_for_task completes / raises on failed
  4) login() refuses to run without a caller-provided reCAPTCHA token
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pixaipy import PixAI, PixAIError  # noqa: E402


class FakeResponse:
    def __init__(self, payload=None, status=200, headers=None):
        self._payload = payload or {}
        self.status_code = status
        self.headers = headers or {}

    def json(self):
        return self._payload


class FakeSession:
    """Scripted request target — returns queued responses per endpoint."""

    def __init__(self):
        self.responses = []
        self.requests = []
        self.headers = {"User-Agent": "UA/test"}

    def request(self, method, url, **kwargs):
        self.requests.append((method, url, kwargs))
        if self.responses:
            return self.responses.pop(0)
        return FakeResponse({}, 500)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)


def graphql_ok(data):
    return FakeResponse({"data": data})


class Smoke(unittest.TestCase):
    def setUp(self):
        self.client = PixAI(token="tok_test")
        self.fake = FakeSession()
        self.client.session = self.fake

    def test_01_quota(self):
        self.fake.responses = [
            graphql_ok({"me": {"id": 1, "email": "e@x", "quotaAmount": 4200}}),
            graphql_ok({"me": {"id": 1, "email": "e@x", "quotaAmount": 4200}}),
        ]
        self.assertEqual(self.client.quota(), 4200)
        self.assertEqual(self.client.me()["email"], "e@x")

    def test_02_persisted_hash_drift_fallback(self):
        self.fake.responses = [
            FakeResponse({"errors": [{"message": "PersistedQueryNotFound",
                                      "extensions": {"code": "PERSISTED_QUERY_NOT_FOUND"}}]}),
            graphql_ok({"me": {"id": 1, "quotaAmount": 7}}),
        ]
        # create_generation_task uses the persisted hash + inline fallback
        task = self.client.create_generation_task("a landscape", model_id="1")
        self.assertEqual(task, {})
        two_calls = self.fake.requests
        self.assertEqual(len(two_calls), 2)
        first_payload = two_calls[0][2]["json"]
        second_payload = two_calls[1][2]["json"]
        self.assertIn("persistedQuery", first_payload["extensions"])
        self.assertNotIn("extensions", second_payload)
        self.assertIn("query", second_payload)

    def test_03_wait_for_task(self):
        # completed path
        self.fake.responses = [
            FakeResponse({"id": "t1", "status": "running"}),
            FakeResponse({"id": "t1", "status": "completed", "outputs": {"mediaUrls": ["https://x/img.png"]}}),
        ]
        statuses = []
        final = self.client.wait_for_task("t1", timeout=10, interval=0, on_status=lambda s, t: statuses.append(s))
        self.assertEqual(final["status"], "completed")
        self.assertEqual(self.client.task_media_urls(final), ["https://x/img.png"])
        # failed path -> PixAIError
        self.fake.responses = [FakeResponse({"id": "t1", "status": "failed"})]
        with self.assertRaises(PixAIError):
            self.client.wait_for_task("t1", timeout=10, interval=0)

    def test_04_cancel_task(self):
        self.fake.responses.append(graphql_ok({"cancelTask": {"id": "t1", "status": "cancelled"}}))
        self.assertTrue(self.client.cancel_task("t1"))

    def test_05_login_needs_recaptcha_token(self):
        with self.assertRaises(PixAIError):
            self.client.login("a@b.c", "pw", recaptcha_token=None)

    def test_06_rest_and_auth_error(self):
        self.fake.responses = [FakeResponse({"error": "x"}, status=401)]
        with self.assertRaises(PixAIError):
            self.client.task("t1")
        self.fake.responses = [FakeResponse({"id": "t1", "status": "completed"})]
        self.assertEqual(self.client.task("t1")["status"], "completed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
