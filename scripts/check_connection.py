"""Notion 페이지 접근 권한과 Markdown 조회 가능 여부를 확인하는 CLI 스크립트."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from notionkit.client import NotionAPIError, NotionMarkdownClient
from notionkit.settings import load_settings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Notion 페이지 접근 권한과 Markdown 조회를 테스트합니다."
    )
    parser.add_argument(
        "--page-id",
        required=True,
        help="테스트할 Notion Page ID",
    )

    args = parser.parse_args()

    settings = load_settings()
    client = NotionMarkdownClient(
        notion_token=settings.notion_token,
        notion_version=settings.notion_version,
    )

    try:
        result = client.retrieve_page_markdown(args.page_id)
    except NotionAPIError as error:
        print("Notion 연결 테스트 실패")
        print(error)
        raise SystemExit(1)

    markdown = result.get("markdown", "")

    print("Notion 연결 테스트 성공")
    print(f"page_id: {result.get('id')}")
    print(f"truncated: {result.get('truncated')}")
    print(f"markdown_length: {len(markdown)}")

    if markdown:
        print("\n--- preview ---")
        print(markdown[:500])


if __name__ == "__main__":
    main()
