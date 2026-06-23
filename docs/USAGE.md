# Usage

저장소를 클론한 뒤 Notion 페이지를 처음 동기화하기까지의 절차이다.

## Prerequisites

* Python 3.12+
* Notion Integration Token
* Integration이 연결된 Notion 페이지

## 설치

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 환경 설정

`.env.example`을 복사하고 토큰을 입력한다.

```powershell
Copy-Item .env.example .env
```

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

## Notion 페이지 연결

페이지 오른쪽 위 `...` > `Connections`에서 Integration을 추가한다. URL에서 Page ID를 복사한다 (32자리 문자열 또는 UUID).

## 페이지 매핑

```powershell
Copy-Item config\pages.example.json config\pages.json
```

`config/pages.json`에 Page ID와 Markdown 파일 경로를 입력한다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "YOUR_PAGE_ID",
    "file": "notes/sample.md"
  }
}
```

`sample`은 명령에서 사용할 페이지 키다.

## 연결 확인

```powershell
python scripts\check_connection.py --page-id "YOUR_PAGE_ID"
```

성공 시:

```text
Notion 연결 테스트 성공
page_id: ...
truncated: False
markdown_length: ...
```

## 동기화

대상 확인:

```powershell
python scripts\sync_page.py --page sample --dry-run
```

실행:

```powershell
python scripts\sync_page.py --page sample
```

`notes/sample.md`를 읽고, 기존 Notion 내용을 `backup/`에 저장한 뒤 Markdown 파일로 교체한다.

## 여러 페이지

```powershell
python scripts\sync_page.py --all --dry-run
python scripts\sync_page.py --all
```

일부 페이지가 실패해도 나머지는 계속 실행되며, 마지막에 실패 목록이 출력된다.

## 로그

```powershell
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

## 자주 쓰는 명령

```powershell
# 연결 확인
python scripts\check_connection.py --page-id "YOUR_PAGE_ID"

# 단일 페이지 dry-run / 동기화
python scripts\sync_page.py --page sample --dry-run
python scripts\sync_page.py --page sample

# 전체 페이지 dry-run / 동기화
python scripts\sync_page.py --all --dry-run
python scripts\sync_page.py --all

# 로그 저장
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

## 문제 해결

| 상황 | 확인할 것 |
| --- | --- |
| `NOTION_TOKEN` 오류 | `.env`와 토큰 값 확인 |
| 404 오류 | 페이지에 Integration 연결 여부 확인 |
| Markdown 파일 없음 | `config/pages.json`의 `file` 경로 확인 |
| 페이지 내용 교체 실패 | child page나 database 포함 여부 확인 |
| 잘못 덮어씀 | `backup/`의 백업 파일 확인 |

자세한 옵션은 [Command Reference](REFERENCE.md)를 참고한다.
