import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from notionkit.client import NotionAPIError, NotionMarkdownClient
from notionkit.settings import load_settings


def load_page_mapping(config_path: str) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"페이지 매핑 설정 파일을 찾을 수 없습니다: {config_path}\n"
            f"config/pages.example.json을 복사해서 config/pages.json을 만드세요."
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_markdown(markdown_path: str) -> str:
    path = Path(markdown_path)

    if not path.exists():
        raise FileNotFoundError(f"Markdown 파일을 찾을 수 없습니다: {markdown_path}")

    return path.read_text(encoding="utf-8")


def resolve_sync_target(args: argparse.Namespace) -> tuple[str, str, str]:
    if args.page_id and args.file:
        return "direct", args.page_id, args.file

    if args.page:
        page_mapping = load_page_mapping(args.config)

        if args.page not in page_mapping:
            available_pages = ", ".join(page_mapping.keys())
            raise KeyError(
                f"페이지 키를 찾을 수 없습니다: {args.page}\n"
                f"사용 가능한 페이지 키: {available_pages}"
            )

        page_info = page_mapping[args.page]

        return (
            page_info.get("title", args.page),
            page_info["page_id"],
            page_info["file"],
        )

    raise ValueError(
        "동기화 대상을 지정해야 합니다. "
        "--page 또는 --page-id와 --file을 사용하세요."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Markdown 파일 내용을 Notion 페이지에 동기화합니다."
    )

    parser.add_argument(
        "--page",
        help="config/pages.json에 정의된 페이지 키",
    )
    parser.add_argument(
        "--page-id",
        help="직접 지정할 Notion Page ID",
    )
    parser.add_argument(
        "--file",
        help="직접 지정할 Markdown 파일 경로",
    )
    parser.add_argument(
        "--config",
        default="config/pages.json",
        help="페이지 매핑 설정 파일 경로",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 Notion 수정 없이 동기화 대상만 확인합니다.",
    )
    parser.add_argument(
        "--allow-deleting-content",
        action="store_true",
        help="child page/database 삭제가 필요한 교체 작업을 허용합니다.",
    )

    args = parser.parse_args()

    title, page_id, markdown_path = resolve_sync_target(args)
    markdown = read_markdown(markdown_path)

    print("동기화 대상 확인")
    print(f"title: {title}")
    print(f"page_id: {page_id}")
    print(f"file: {markdown_path}")
    print(f"markdown_length: {len(markdown)}")

    if args.dry_run:
        print("dry-run 모드이므로 Notion 페이지를 수정하지 않습니다.")
        return

    settings = load_settings()
    client = NotionMarkdownClient(
        notion_token=settings.notion_token,
        notion_version=settings.notion_version,
    )

    try:
        result = client.replace_page_markdown(
            page_id=page_id,
            markdown=markdown,
            allow_deleting_content=args.allow_deleting_content,
        )
    except NotionAPIError as error:
        print("Notion 페이지 동기화 실패")
        print(error)
        raise SystemExit(1)

    print("Notion 페이지 동기화 완료")
    print(f"page_id: {result.get('id')}")
    print(f"truncated: {result.get('truncated')}")
    print(f"updated_markdown_length: {len(result.get('markdown', ''))}")


if __name__ == "__main__":
    main()
