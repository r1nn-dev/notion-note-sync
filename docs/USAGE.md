# Usage

## Environment Setup

`.env.example`을 복사해 `.env`를 만든다.

```powershell
Copy-Item .env.example .env
```

macOS나 Linux에서는 다음 명령을 사용한다.

```bash
cp .env.example .env
```

`.env`에는 실제 Notion Integration Token과 Notion API 버전을 입력한다.

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

Notion API 버전은 Notion에서 허용하는 날짜 값이어야 한다.

## Install

가상환경을 만든다.

```powershell
python -m venv .venv
```

PowerShell에서 가상환경을 활성화한다.

```powershell
.venv\Scripts\Activate.ps1
```

필요한 패키지를 설치한다.

```powershell
pip install -r requirements.txt
```

## Test

단위 테스트는 `pytest`로 실행한다.

```powershell
python -m pytest
```

공개 저장소 전환 전 보안 점검은 다음 명령으로 실행한다.

```powershell
python scripts\check_public_ready.py
```

## Notion Page Connection

Notion Integration을 만든 뒤, 동기화할 Notion 페이지에 해당 Integration을 연결해야 한다.

페이지가 Integration에 공유되지 않으면 API 요청은 404로 실패한다. 이때 응답에는 보통 `object_not_found`와 함께 페이지를 Integration에 공유하라는 메시지가 나온다.

확인 순서는 다음과 같다.

1. Notion에서 대상 페이지를 연다.
2. 오른쪽 위 `Share` 또는 `...` 메뉴를 연다.
3. `Connections`에서 이 프로젝트의 Integration을 추가한다.
4. Page ID를 `config/pages.json`에 저장한다.

## Page Mapping

`config/pages.example.json`을 참고해 `config/pages.json`을 만든다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "file": "notes/sample.md"
  }
}
```

각 항목의 의미는 다음과 같다.

* `sample`: 명령에서 사용할 페이지 키이다.
* `title`: 사람이 구분하기 위한 이름이다.
* `page_id`: Notion Page ID이다.
* `file`: Notion에 반영할 Markdown 파일 경로이다.

`page_id`와 `file`은 필수 값이며 비어 있으면 동기화를 시작하지 않는다. `title`을 생략하면 페이지 키를 제목으로 사용한다.

## Check Connection

Notion 페이지 접근 권한과 Markdown 조회 가능 여부를 확인한다.

```powershell
python scripts\check_connection.py --page-id "NOTION_PAGE_ID"
```

정상 연결되면 페이지 ID, Markdown 길이, 일부 미리보기 내용이 출력된다.

## Sync

설정 파일에 등록한 페이지 키로 실행한다.

```powershell
python scripts\sync_page.py --page sample
```

설정 파일에 등록한 모든 페이지를 실행하려면 `--all`을 사용한다.

```powershell
python scripts\sync_page.py --all
```

전체 동기화 중 일부 페이지가 실패하면 나머지 페이지를 계속 시도한 뒤 성공/실패 개수와 실패 상세를 출력한다.

실제 Notion 페이지를 수정하지 않고 대상만 확인하려면 `--dry-run`을 사용한다.

```powershell
python scripts\sync_page.py --page sample --dry-run
```

전체 동기화도 dry-run으로 먼저 확인할 수 있다.

```powershell
python scripts\sync_page.py --all --dry-run
```

실행 결과를 파일로 남기려면 `--log-file`을 사용한다.

```powershell
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

Page ID와 Markdown 파일을 직접 지정할 수도 있다.

```powershell
python scripts\sync_page.py --page-id "NOTION_PAGE_ID" --file "notes/sample.md"
```

기본 동기화는 Notion 페이지를 교체하기 전에 기존 Markdown을 `backup/` 디렉터리에 저장한다.

```powershell
python scripts\sync_page.py --page sample --backup-dir "backup/notion"
```

백업 없이 바로 동기화하려면 `--skip-backup`을 사용한다.

```powershell
python scripts\sync_page.py --page sample --skip-backup
```

Notion 페이지 안에 child page나 database가 있으면 내용 교체가 막힐 수 있다. 그런 항목 삭제가 필요한 교체 작업을 허용하려면 다음 옵션을 사용한다.

```powershell
python scripts\sync_page.py --page sample --allow-deleting-content
```

Notion API가 rate limit 또는 일시적인 서버 오류를 반환하면 자동으로 재시도한다. `Retry-After` 헤더가 있으면 해당 대기 시간을 우선 사용한다.
