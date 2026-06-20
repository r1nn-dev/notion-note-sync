# Notion Note Sync

로컬 Markdown 파일을 Notion 페이지에 반영하는 Python CLI 도구이다.

Notion 페이지를 웹에서 직접 열어 내용을 복사하고 붙여넣는 대신, 로컬에서 작성한 Markdown 파일을 기준으로 지정한 Notion 페이지를 갱신한다. 여러 페이지를 `config/pages.json`으로 관리하고, 동기화 전 기존 Notion 내용을 자동 백업한다.

## What It Does

* Notion Integration Token을 `.env`에서 읽는다.
* Notion 페이지 접근 권한과 Markdown 조회 가능 여부를 확인한다.
* Markdown 파일 내용을 Notion 페이지 Markdown으로 교체한다.
* `config/pages.json`에 등록한 페이지 키로 동기화 대상을 선택한다.
* 등록된 모든 페이지를 `--all`로 일괄 동기화한다.
* 실제 수정 전 `--dry-run`으로 대상과 파일 길이를 확인한다.
* 동기화 전 기존 Notion Markdown을 `backup/`에 저장한다.
* API 일시 오류와 rate limit에 대해 재시도한다.
* 실행 로그를 `--log-file`로 파일에 남긴다.
* 일괄 동기화 결과를 성공/실패 개수와 실패 상세로 요약한다.

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
Copy-Item config\pages.example.json config\pages.json
```

`.env`에 Notion Integration Token을 입력한다.

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

`config/pages.json`에 Notion Page ID와 Markdown 파일 경로를 입력한다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "file": "notes/sample.md"
  }
}
```

Notion 연결을 확인한다.

```powershell
python scripts\check_connection.py --page-id "NOTION_PAGE_ID"
```

동기화 대상을 먼저 확인한다.

```powershell
python scripts\sync_page.py --page sample --dry-run
```

실제 동기화를 실행한다.

```powershell
python scripts\sync_page.py --page sample
```

등록된 모든 페이지를 동기화한다.

```powershell
python scripts\sync_page.py --all
```

## Documentation

* [Usage](docs/USAGE.md): 설치, 설정, 연결 확인, 동기화 명령 전체 사용법
* [Security](docs/SECURITY.md): 토큰, Page ID, 개인 노트, 백업/로그 파일 관리 기준
* [Project Status](docs/STATUS.md): 구현된 기능과 아직 없는 기능

## Project Structure

```text
notion-note-sync/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── config/
│   ├── pages.example.json
│   └── pages.json
├── docs/
│   ├── SECURITY.md
│   ├── STATUS.md
│   └── USAGE.md
├── notes/
│   └── sample.md
├── notionkit/
│   ├── __init__.py
│   ├── client.py
│   └── settings.py
├── scripts/
│   ├── check_connection.py
│   ├── check_public_ready.py
│   └── sync_page.py
└── tests/
    ├── test_check_public_ready.py
    ├── test_client.py
    └── test_sync_page.py
```

## Commit Message Convention

이 프로젝트는 Conventional Commits 형식을 참고한다.

```text
type(scope): description
```

예시:

```text
feat(sync): implement markdown page sync command
fix(auth): handle missing notion token
docs(readme): update project documentation
test(sync): add sync page test cases
security: add public readiness check
```

## License

현재 별도 라이선스를 지정하지 않는다.
