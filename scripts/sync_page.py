import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from notionkit.client import NotionAPIError, NotionMarkdownClient
from notionkit.settings import load_settings


SyncTarget = tuple[str, str, str]


def load_page_mapping(config_path: str) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"페이지 매핑 설정 파일을 찾을 수 없습니다: {config_path}\n"
            "config/pages.example.json을 복사해서 config/pages.json을 만드세요."
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_markdown(markdown_path: str) -> str:
    path = Path(markdown_path)

    if not path.exists():
        raise FileNotFoundError(f"Markdown 파일을 찾을 수 없습니다: {markdown_path}")

    return path.read_text(encoding="utf-8")


def resolve_sync_targets(args: argparse.Namespace) -> list[SyncTarget]:
    if args.all:
        if args.page or args.page_id or args.file:
            raise ValueError("--all은 --page, --page-id, --file과 함께 사용할 수 없습니다.")

        page_mapping = load_page_mapping(args.config)
        return [
            (
                page_info.get("title", page_key),
                page_info["page_id"],
                page_info["file"],
            )
            for page_key, page_info in page_mapping.items()
        ]

    if args.page_id and args.file:
        return [("direct", args.page_id, args.file)]

    if args.page_id or args.file:
        raise ValueError("--page-id와 --file은 함께 사용해야 합니다.")

    if args.page:
        page_mapping = load_page_mapping(args.config)

        if args.page not in page_mapping:
            available_pages = ", ".join(page_mapping.keys())
            raise KeyError(
                f"페이지 키를 찾을 수 없습니다: {args.page}\n"
                f"사용 가능한 페이지: {available_pages}"
            )

        page_info = page_mapping[args.page]

        return [
            (
                page_info.get("title", args.page),
                page_info["page_id"],
                page_info["file"],
            )
        ]

    raise ValueError(
        "동기화 대상을 지정해야 합니다. "
        "--page, --all 또는 --page-id와 --file을 함께 사용하세요."
    )


def make_safe_filename(value: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return safe_name or "notion-page"


def save_backup(
    client: NotionMarkdownClient,
    title: str,
    page_id: str,
    backup_dir: str,
) -> Path:
    result = client.retrieve_page_markdown(page_id)
    markdown = result.get("markdown", "")

    backup_path = Path(backup_dir)
    if not backup_path.is_absolute():
        backup_path = PROJECT_ROOT / backup_path

    backup_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{make_safe_filename(title)}-{page_id[:8]}.md"
    output_path = backup_path / filename
    output_path.write_text(markdown, encoding="utf-8")

    return output_path


def sync_target(
    client: NotionMarkdownClient | None,
    title: str,
    page_id: str,
    markdown_path: str,
    *,
    dry_run: bool,
    skip_backup: bool,
    backup_dir: str,
    allow_deleting_content: bool,
) -> None:
    markdown = read_markdown(markdown_path)

    print("동기화 대상 확인")
    print(f"title: {title}")
    print(f"page_id: {page_id}")
    print(f"file: {markdown_path}")
    print(f"markdown_length: {len(markdown)}")

    if dry_run:
        print("dry-run 모드입니다. Notion 페이지를 수정하지 않습니다.")
        return

    if client is None:
        raise RuntimeError("Notion client가 초기화되지 않았습니다.")

    if not skip_backup:
        backup_path = save_backup(
            client=client,
            title=title,
            page_id=page_id,
            backup_dir=backup_dir,
        )
        print(f"기존 Notion Markdown 백업 완료: {backup_path}")

    result = client.replace_page_markdown(
        page_id=page_id,
        markdown=markdown,
        allow_deleting_content=allow_deleting_content,
    )

    print("Notion 페이지 동기화 완료")
    print(f"page_id: {result.get('id')}")
    print(f"truncated: {result.get('truncated')}")
    print(f"updated_markdown_length: {len(result.get('markdown', ''))}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Markdown 파일 내용을 Notion 페이지에 동기화합니다."
    )

    parser.add_argument(
        "--page",
        help="config/pages.json에 정의된 페이지 키",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="config/pages.json에 정의된 모든 페이지를 동기화합니다.",
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
        help="실제 Notion 페이지를 수정하지 않고 동기화 대상만 확인합니다.",
    )
    parser.add_argument(
        "--allow-deleting-content",
        action="store_true",
        help="child page/database 삭제가 필요한 전체 교체 작업을 허용합니다.",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="동기화 전에 기존 Notion Markdown을 백업하지 않습니다.",
    )
    parser.add_argument(
        "--backup-dir",
        default="backup",
        help="기존 Notion Markdown 백업을 저장할 디렉터리",
    )

    args = parser.parse_args()

    try:
        targets = resolve_sync_targets(args)
    except (FileNotFoundError, KeyError, ValueError) as error:
        parser.error(str(error))

    if args.all:
        print(f"전체 동기화 대상: {len(targets)}개")

    client = None
    if not args.dry_run:
        settings = load_settings()
        client = NotionMarkdownClient(
            notion_token=settings.notion_token,
            notion_version=settings.notion_version,
        )

    failed_targets: list[str] = []
    for index, (title, page_id, markdown_path) in enumerate(targets, start=1):
        if len(targets) > 1:
            print(f"\n[{index}/{len(targets)}]")

        try:
            sync_target(
                client=client,
                title=title,
                page_id=page_id,
                markdown_path=markdown_path,
                dry_run=args.dry_run,
                skip_backup=args.skip_backup,
                backup_dir=args.backup_dir,
                allow_deleting_content=args.allow_deleting_content,
            )
        except (FileNotFoundError, KeyError, NotionAPIError, RuntimeError) as error:
            print("Notion 페이지 동기화 실패")
            print(error)
            failed_targets.append(title)

            if len(targets) == 1:
                raise SystemExit(1)

    if failed_targets:
        print(f"\n실패한 동기화 대상: {', '.join(failed_targets)}")
        raise SystemExit(1)

    if len(targets) > 1:
        print(f"\n전체 동기화 완료: {len(targets)}개")


if __name__ == "__main__":
    main()
