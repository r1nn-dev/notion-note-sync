from typing import Any

import requests


class NotionAPIError(RuntimeError):
    pass


class NotionMarkdownClient:
    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, notion_token: str, notion_version: str) -> None:
        self.notion_token = notion_token
        self.notion_version = notion_version

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

        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            timeout=30,
            **kwargs,
        )

        if response.status_code >= 400:
            raise NotionAPIError(
                "Notion API 요청 실패\n"
                f"status_code={response.status_code}\n"
                f"response={response.text}"
            )

        return response.json()

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
