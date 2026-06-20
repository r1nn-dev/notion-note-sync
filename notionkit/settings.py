import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    notion_token: str
    notion_version: str


def load_settings(env_path: str = ".env") -> Settings:
    load_dotenv(env_path)

    notion_token = os.getenv("NOTION_TOKEN")
    notion_version = os.getenv("NOTION_VERSION", "2026-03-11")

    if not notion_token:
        raise RuntimeError(
            "NOTION_TOKEN이 설정되어 있지 않습니다. "
            ".env 파일을 만들고 Notion Integration Token을 입력하세요."
        )

    return Settings(
        notion_token=notion_token,
        notion_version=notion_version,
    )