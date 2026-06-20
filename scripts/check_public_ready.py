"""Public repository readiness checks for local secrets and private files."""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BLOCKED_TRACKED_PATHS = {
    ".env",
    "config/pages.json",
}
BLOCKED_TRACKED_PREFIXES = (
    "backup/",
    "logs/",
    "notes/private/",
)
ALLOWED_TRACKED_PATHS = {
    ".env.example",
}
SECRET_PATTERNS = {
    "notion_token": re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9_-]{20,}\b"),
    "notion_page_id": re.compile(
        r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b"
    ),
}


@dataclass(frozen=True)
class PublicReadyFinding:
    path: str
    issue: str


def normalize_git_path(path: str) -> str:
    return path.replace("\\", "/")


def list_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return [
        normalize_git_path(line.strip())
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def find_blocked_tracked_paths(paths: list[str]) -> list[PublicReadyFinding]:
    findings: list[PublicReadyFinding] = []

    for path in paths:
        if path in ALLOWED_TRACKED_PATHS:
            continue

        if path in BLOCKED_TRACKED_PATHS:
            findings.append(
                PublicReadyFinding(path=path, issue="로컬 전용 파일이 Git에 추적됩니다.")
            )
            continue

        if path.startswith(".env.") or path.startswith(BLOCKED_TRACKED_PREFIXES):
            findings.append(
                PublicReadyFinding(path=path, issue="비공개 경로의 파일이 Git에 추적됩니다.")
            )

    return findings


def scan_file_for_sensitive_values(path: str) -> list[PublicReadyFinding]:
    file_path = PROJECT_ROOT / path
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[PublicReadyFinding] = []
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(content):
            findings.append(
                PublicReadyFinding(path=path, issue=f"민감 값 패턴이 발견됐습니다: {name}")
            )

    return findings


def run_public_ready_checks(paths: list[str]) -> list[PublicReadyFinding]:
    findings = find_blocked_tracked_paths(paths)

    for path in paths:
        findings.extend(scan_file_for_sensitive_values(path))

    return findings


def main() -> None:
    try:
        tracked_files = list_tracked_files()
    except subprocess.CalledProcessError as error:
        print("Git 추적 파일 목록을 읽지 못했습니다.")
        print(error)
        raise SystemExit(1)

    findings = run_public_ready_checks(tracked_files)

    if not findings:
        print("공개 준비 점검 통과")
        return

    print("공개 준비 점검 실패")
    for finding in findings:
        print(f"- {finding.path}: {finding.issue}")

    raise SystemExit(1)


if __name__ == "__main__":
    main()
