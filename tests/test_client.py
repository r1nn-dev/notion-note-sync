from unittest.mock import Mock, patch

import pytest

from notionkit.client import NotionAPIError, NotionMarkdownClient


def make_response(
    status_code: int,
    *,
    headers: dict[str, str] | None = None,
    body: dict[str, object] | None = None,
) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.headers = headers or {}
    response.text = str(body or {})
    response.json.return_value = body or {}
    return response


def test_request_retries_rate_limited_response_with_retry_after() -> None:
    rate_limited = make_response(429, headers={"Retry-After": "2"})
    success = make_response(200, body={"ok": True})
    client = NotionMarkdownClient("token", "2026-03-11")

    with patch(
        "notionkit.client.requests.request",
        side_effect=[rate_limited, success],
    ) as request:
        with patch("notionkit.client.time.sleep") as sleep:
            result = client._request("GET", "/pages/page-id/markdown")

    assert result == {"ok": True}
    assert request.call_count == 2
    sleep.assert_called_once_with(2.0)


def test_request_raises_after_retry_limit() -> None:
    client = NotionMarkdownClient("token", "2026-03-11", max_retries=1)

    with patch(
        "notionkit.client.requests.request",
        return_value=make_response(503, body={"error": "unavailable"}),
    ):
        with patch("notionkit.client.time.sleep"):
            with pytest.raises(NotionAPIError, match="status_code=503"):
                client._request("GET", "/pages/page-id/markdown")
