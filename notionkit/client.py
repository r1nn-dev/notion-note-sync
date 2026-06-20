import time
from typing import Any

import requests


class NotionAPIError(RuntimeError):
    pass


class NotionMarkdownClient:
    BASE_URL = "https://api.notion.com/v1"
    RETRY_STATUS_CODES = {429, 500, 503, 504, 529}

    def __init__(
        self,
        notion_token: str,
        notion_version: str,
        max_retries: int = 3,
        retry_backoff_seconds: float = 1.0,
    ) -> None:
        self.notion_token = notion_token
        self.notion_version = notion_version
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        url = f"{self.BASE_URL}{path}"

        for attempt in range(self.max_retries + 1):
            response = requests.request(
                method=method,
                url=url,
                headers=self._headers(),
                timeout=30,
                **kwargs,
            )

            if not self._should_retry(response, attempt):
                break

            time.sleep(self._retry_delay(response, attempt))

        if response.status_code >= 400:
            raise NotionAPIError(
                "Notion API 요청 실패\n"
                f"status_code={response.status_code}\n"
                f"response={response.text}"
            )

        return response.json()

    def _should_retry(self, response: requests.Response, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False

        return response.status_code in self.RETRY_STATUS_CODES

    def _retry_delay(self, response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass

        return self.retry_backoff_seconds * (2**attempt)

    def retrieve_page_markdown(self, page_id: str) -> dict[str, Any]:
        return self._request(
            method="GET",
            path=f"/pages/{page_id}/markdown",
        )

    def replace_page_markdown(
        self,
        page_id: str,
        markdown: str,
        allow_deleting_content: bool = False,
    ) -> dict[str, Any]:
        payload = {
            "type": "replace_content",
            "replace_content": {
                "new_str": markdown,
                "allow_deleting_content": allow_deleting_content,
            },
        }

        return self._request(
            method="PATCH",
            path=f"/pages/{page_id}/markdown",
            json=payload,
        )
