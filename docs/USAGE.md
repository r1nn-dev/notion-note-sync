# Usage

이 문서는 `notion-note-sync`를 실제로 실행하기 위한 절차를 정리한다. 처음 설정할 때는 위에서 아래 순서대로 진행하고, 이후에는 “자주 쓰는 명령”만 보면 된다.

## 1. 설치

프로젝트 루트에서 가상환경을 만든다.

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

테스트가 실행되는지 확인한다.

```powershell
python -m pytest
```

## 2. Notion Integration 준비

Notion API를 사용하려면 Notion Integration Token이 필요하다.

1. Notion에서 Integration을 만든다.
2. Internal Integration Token을 복사한다.
3. 동기화할 Notion 페이지에 Integration을 연결한다.
4. 동기화할 페이지의 Page ID를 확인한다.

페이지가 Integration에 공유되지 않으면 API 요청은 보통 404 `object_not_found`로 실패한다.

## 3. `.env` 설정

예시 파일을 복사한다.

```powershell
Copy-Item .env.example .env
```

`.env`에 실제 토큰을 입력한다.

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

`NOTION_TOKEN`은 필수 값이다. `NOTION_VERSION`을 생략하면 코드에서 기본값 `2026-03-11`을 사용한다.

## 4. 페이지 매핑 설정

예시 파일을 복사한다.

```powershell
Copy-Item config\pages.example.json config\pages.json
```

`config/pages.json`에 동기화할 페이지를 등록한다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "file": "notes/sample.md"
  }
}
```

필드 설명:

| 필드 | 필수 | 설명 |
| --- | --- | --- |
| `sample` | 예 | 명령에서 사용할 페이지 키 |
| `title` | 아니오 | 출력과 백업 파일명에 사용할 표시 이름 |
| `page_id` | 예 | Notion Page ID |
| `file` | 예 | Notion에 반영할 로컬 Markdown 파일 경로 |

`title`을 생략하면 페이지 키를 제목으로 사용한다. `page_id`나 `file`이 비어 있으면 동기화를 시작하지 않는다.

## 5. 연결 확인

Notion 페이지 접근 권한과 Markdown 조회 가능 여부를 확인한다.

```powershell
python scripts\check_connection.py --page-id "NOTION_PAGE_ID"
```

성공하면 다음 정보가 출력된다.

```text
Notion 연결 테스트 성공
page_id: ...
truncated: ...
markdown_length: ...
```

## 6. 동기화 전 확인

처음에는 반드시 `--dry-run`으로 대상만 확인한다.

```powershell
python scripts\sync_page.py --page sample --dry-run
```

출력 예:

```text
동기화 대상 확인
title: Sample Notion Page
page_id: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
file: notes/sample.md
markdown_length: 329
dry-run 모드입니다. Notion 페이지를 수정하지 않습니다.
```

`--all`도 dry-run으로 확인할 수 있다.

```powershell
python scripts\sync_page.py --all --dry-run
```

## 7. 실제 동기화

설정 파일에 등록한 페이지 하나를 동기화한다.

```powershell
python scripts\sync_page.py --page sample
```

등록된 모든 페이지를 순서대로 동기화한다.

```powershell
python scripts\sync_page.py --all
```

`--all` 실행 중 일부 페이지가 실패해도 나머지 페이지는 계속 시도한다. 마지막에는 성공/실패 개수와 실패 상세가 출력된다.

```text
동기화 요약
성공: 2개
실패: 1개
실패 상세:
- Lecture Note: Markdown 파일을 찾을 수 없습니다: notes/lecture.md
```

## 8. 백업

기본 동작은 Notion 페이지를 교체하기 전에 기존 Notion Markdown을 받아 `backup/`에 저장하는 것이다.

백업 파일명 형식:

```text
YYYYMMDD-HHMMSS-title-pageid.md
```

백업 디렉터리를 바꾸려면 `--backup-dir`을 사용한다.

```powershell
python scripts\sync_page.py --page sample --backup-dir "backup/notion"
```

백업 없이 바로 동기화하려면 `--skip-backup`을 사용한다.

```powershell
python scripts\sync_page.py --page sample --skip-backup
```

`--skip-backup`은 테스트 페이지가 아니면 권장하지 않는다.

## 9. 로그 파일

콘솔 출력과 오류를 파일에도 남기려면 `--log-file`을 사용한다.

```powershell
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

상대 경로는 프로젝트 루트 기준이다. 필요한 디렉터리는 자동으로 생성된다.

## 10. 직접 Page ID와 파일 지정

`config/pages.json`을 사용하지 않고 Page ID와 Markdown 파일을 직접 지정할 수 있다.

```powershell
python scripts\sync_page.py --page-id "NOTION_PAGE_ID" --file "notes/sample.md"
```

`--page-id`와 `--file`은 반드시 함께 사용해야 한다.

## 11. Child Page 또는 Database가 있는 페이지

Notion 페이지 안에 child page나 database가 있으면 전체 내용 교체가 막힐 수 있다. 그런 항목 삭제가 필요한 교체 작업을 허용하려면 다음 옵션을 사용한다.

```powershell
python scripts\sync_page.py --page sample --allow-deleting-content
```

이 옵션은 Notion 페이지 내부 구조를 삭제할 수 있으므로 필요한 경우에만 사용한다.

## 12. 명령 요약

| 작업 | 명령 |
| --- | --- |
| 연결 확인 | `python scripts\check_connection.py --page-id "NOTION_PAGE_ID"` |
| 단일 페이지 dry-run | `python scripts\sync_page.py --page sample --dry-run` |
| 단일 페이지 동기화 | `python scripts\sync_page.py --page sample` |
| 전체 페이지 dry-run | `python scripts\sync_page.py --all --dry-run` |
| 전체 페이지 동기화 | `python scripts\sync_page.py --all` |
| 로그 저장 | `python scripts\sync_page.py --all --log-file "logs/sync.log"` |
| 백업 생략 | `python scripts\sync_page.py --page sample --skip-backup` |
| 보안 점검 | `python scripts\check_public_ready.py` |

## 13. 문제 해결

| 증상 | 확인할 것 |
| --- | --- |
| `NOTION_TOKEN` 오류 | `.env`가 있고 `NOTION_TOKEN` 값이 입력되어 있는지 확인 |
| 404 `object_not_found` | 페이지가 Integration에 공유되어 있는지 확인 |
| `missing_version` | `NOTION_VERSION` 값이 올바른 날짜 형식인지 확인 |
| Markdown 파일 없음 | `config/pages.json`의 `file` 경로가 실제 파일과 일치하는지 확인 |
| child page/database 오류 | 정말 전체 교체가 필요한 경우에만 `--allow-deleting-content` 사용 |
| 일부 페이지만 실패 | `--all` 실행 마지막의 실패 상세 확인 |

## 14. API 재시도

Notion API가 다음 상태 코드를 반환하면 자동으로 재시도한다.

```text
429, 500, 503, 504, 529
```

응답에 `Retry-After` 헤더가 있으면 해당 값을 우선 사용한다. 없으면 짧은 backoff로 최대 3회 재시도한다.
