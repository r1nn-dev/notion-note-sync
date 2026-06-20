# Notion Note Sync

Markdown으로 관리하는 개인 노트를 Notion 페이지에 동기화하는 Python 자동화 프로젝트이다.

강의 노트, 학습 기록, 기술 문서 초안을 로컬 Markdown 파일로 작성하고, 필요한 시점에 Notion API를 통해 지정한 페이지에 반영하는 것을 목표로 한다. Notion은 정리와 공유에 편하지만, 반복해서 내용을 복사하거나 페이지를 직접 수정하는 과정은 번거롭다. 이 프로젝트는 그 반복 작업을 줄이기 위한 작은 도구이다.

## Purpose

* Markdown 파일을 기준으로 Notion 페이지 내용을 갱신한다.
* Notion API 인증과 페이지 접근 권한을 별도로 테스트한다.
* 실제 토큰, Page ID, 개인 노트 같은 민감한 값은 공개 파일과 분리한다.
* 여러 Notion 페이지를 설정 파일로 관리할 수 있는 구조를 만든다.
* 나중에 공개 저장소로 전환해도 안전한 프로젝트 형태를 유지한다.

## Features

* `.env`에서 Notion Integration Token과 API 버전을 읽는다.
* Notion 페이지의 Markdown 조회 가능 여부를 확인한다.
* 로컬 Markdown 파일을 읽어 Notion 페이지 내용으로 교체한다.
* `config/pages.json`에 등록한 페이지 키로 동기화 대상을 선택한다.
* `config/pages.json`에 등록한 모든 페이지를 한 번에 동기화한다.
* `--dry-run` 옵션으로 실제 수정 없이 동기화 대상을 확인한다.
* 동기화 전 기존 Notion 페이지 Markdown을 `backup/`에 저장한다.
* Notion API의 일시적인 제한이나 서버 오류가 발생하면 짧게 재시도한다.
* `--log-file` 옵션으로 실행 결과를 파일에 함께 저장한다.
* 전체 동기화에서 실패한 페이지와 실패 이유를 요약한다.

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`에 Notion Integration Token을 입력한 뒤, `config/pages.example.json`을 참고해 `config/pages.json`을 만든다.

연결을 확인한다.

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

등록된 모든 페이지를 동기화하려면 다음 명령을 사용한다.

```powershell
python scripts\sync_page.py --all
```

## Docs

* [Usage](docs/USAGE.md)
* [Security](docs/SECURITY.md)
* [Project Status](docs/STATUS.md)

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

예시는 다음과 같다.

```text
feat(sync): implement markdown page sync command
fix(auth): handle missing notion token
docs(readme): update project documentation
test(sync): add sync page test cases
security: add public readiness check
```

## License

현재 별도 라이선스를 지정하지 않는다.
