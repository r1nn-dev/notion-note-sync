# Usage

이 문서는 저장소를 받은 뒤 Notion 페이지 하나를 실제로 수정하기까지의 최소 절차를 설명한다. 처음 실행할 때는 반드시 테스트용 Notion 페이지로 진행한다.

## 0. 준비물

필요한 것은 네 가지다.

* Python 3.12 이상
* Notion Integration Token
* Integration이 연결된 Notion 테스트 페이지
* 동기화할 Markdown 파일

처음에는 중요한 페이지가 아니라 비어 있는 테스트 페이지를 사용한다. 이 도구는 Notion 페이지 내용을 로컬 Markdown 내용으로 교체한다.

## 1. 프로젝트 설치

저장소를 받은 뒤 프로젝트 폴더로 이동한다.

```powershell
cd notion-note-sync
```

가상환경을 만들고 활성화한다.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

패키지를 설치한다.

```powershell
pip install -r requirements.txt
```

## 2. Notion Token 입력

`.env.example`을 복사한다.

```powershell
Copy-Item .env.example .env
```

`.env`를 열고 `NOTION_TOKEN`에 실제 Integration Token을 넣는다.

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

`NOTION_VERSION`은 그대로 둬도 된다.

## 3. Notion 페이지 연결

Notion에서 테스트 페이지를 연다.

1. 오른쪽 위 `...` 또는 `Share`를 연다.
2. `Connections`에서 만든 Integration을 추가한다.
3. 페이지 URL에서 Page ID를 복사한다.

Page ID는 보통 32자리 문자열이거나 하이픈이 포함된 UUID 형태다.

## 4. 동기화할 Markdown 준비

처음에는 포함된 샘플 파일을 사용한다.

```text
notes/sample.md
```

원하면 이 파일 내용을 짧게 수정한다.

```markdown
# Sample Note

This page was updated from local Markdown.
```

## 5. 페이지 매핑 파일 만들기

예시 파일을 복사한다.

```powershell
Copy-Item config\pages.example.json config\pages.json
```

`config/pages.json`을 열고 `page_id`를 실제 테스트 페이지 ID로 바꾼다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "YOUR_TEST_PAGE_ID",
    "file": "notes/sample.md"
  }
}
```

여기서 `sample`은 명령에서 사용할 이름이다. 다른 이름으로 바꾸면 `--page` 값도 같이 바꿔야 한다.

## 6. 연결 테스트

먼저 Notion API가 페이지를 읽을 수 있는지 확인한다.

```powershell
python scripts\check_connection.py --page-id "YOUR_TEST_PAGE_ID"
```

성공하면 다음처럼 나온다.

```text
Notion 연결 테스트 성공
page_id: ...
truncated: False
markdown_length: ...
```

실패하면 대부분 다음 중 하나다.

* `.env`에 토큰이 잘못 들어갔다.
* Notion 페이지에 Integration이 연결되지 않았다.
* Page ID를 잘못 복사했다.

## 7. 실제 수정 전 dry-run

Notion을 수정하지 않고 어떤 파일이 어떤 페이지로 갈지 확인한다.

```powershell
python scripts\sync_page.py --page sample --dry-run
```

확인할 것:

* `title`이 예상한 페이지 이름인가
* `page_id`가 테스트 페이지 ID인가
* `file`이 수정하려는 Markdown 파일인가
* `markdown_length`가 0이 아닌가

## 8. Notion 페이지 수정 실행

dry-run 결과가 맞으면 실제 동기화를 실행한다.

```powershell
python scripts\sync_page.py --page sample
```

이 명령은 다음 순서로 동작한다.

1. `notes/sample.md`를 읽는다.
2. 기존 Notion 페이지 Markdown을 `backup/`에 저장한다.
3. Notion 페이지 내용을 Markdown 파일 내용으로 교체한다.
4. 결과와 Markdown 길이를 출력한다.

실행 후 Notion 테스트 페이지를 열어 내용이 바뀌었는지 확인한다.

## 9. 백업 확인

동기화가 성공하면 `backup/` 폴더에 이전 Notion 내용이 저장된다.

```text
backup/
└── 20260620-180000-Sample-Notion-Page-xxxxxxxx.md
```

잘못 동기화했다면 이 백업 파일을 열어 이전 내용을 확인할 수 있다.

## 10. 여러 페이지 동기화

`config/pages.json`에 페이지를 여러 개 등록할 수 있다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "YOUR_TEST_PAGE_ID",
    "file": "notes/sample.md"
  },
  "study": {
    "title": "Study Note",
    "page_id": "ANOTHER_PAGE_ID",
    "file": "notes/study.md"
  }
}
```

전체 대상 확인:

```powershell
python scripts\sync_page.py --all --dry-run
```

전체 동기화:

```powershell
python scripts\sync_page.py --all
```

일부 페이지가 실패해도 나머지는 계속 실행되고, 마지막에 실패 목록이 출력된다.

## 11. 로그 남기기

실행 기록을 파일로 남기려면 `--log-file`을 붙인다.

```powershell
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

콘솔에 보이는 내용이 로그 파일에도 같이 저장된다.

## 12. 자주 쓰는 명령

```powershell
# 연결 확인
python scripts\check_connection.py --page-id "YOUR_TEST_PAGE_ID"

# 단일 페이지 확인
python scripts\sync_page.py --page sample --dry-run

# 단일 페이지 동기화
python scripts\sync_page.py --page sample

# 전체 페이지 확인
python scripts\sync_page.py --all --dry-run

# 전체 페이지 동기화
python scripts\sync_page.py --all

# 전체 페이지 동기화 + 로그 저장
python scripts\sync_page.py --all --log-file "logs/sync.log"
```

## 13. 막혔을 때

| 상황 | 해결 |
| --- | --- |
| `NOTION_TOKEN` 오류 | `.env` 파일과 토큰 값을 확인한다. |
| 404 오류 | Notion 페이지에 Integration을 연결했는지 확인한다. |
| Markdown 파일을 찾을 수 없음 | `config/pages.json`의 `file` 경로를 확인한다. |
| 페이지 내용 교체 실패 | 페이지 안에 child page나 database가 있는지 확인한다. |
| 실수로 잘못 덮어씀 | `backup/` 폴더의 백업 Markdown을 확인한다. |

더 자세한 옵션 설명은 [Command Reference](REFERENCE.md)를 참고한다.
