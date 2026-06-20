# Notion Note Sync

Markdown으로 관리하는 개인 노트를 Notion 페이지에 동기화하는 Python 자동화 프로젝트이다.

강의 노트, 학습 기록, 기술 문서 초안을 로컬 Markdown 파일로 작성하고, 필요한 시점에 Notion API를 통해 지정한 페이지에 반영하는 것을 목표로 한다. Notion은 정리와 공유에 편하지만, 반복해서 내용을 복사하거나 페이지를 직접 수정하는 과정은 번거롭다. 이 프로젝트는 그 반복 작업을 줄이기 위한 작은 도구이다.

## 목적

이 프로젝트의 목적은 다음과 같다.

* Markdown 파일을 기준으로 Notion 페이지 내용을 갱신한다.
* Notion API 인증과 페이지 접근 권한을 별도로 테스트한다.
* 실제 토큰, Page ID, 개인 노트 같은 민감한 값은 공개 파일과 분리한다.
* 여러 Notion 페이지를 설정 파일로 관리할 수 있는 구조를 만든다.
* 나중에 공개 저장소로 전환해도 안전한 프로젝트 형태를 유지한다.

## 주요 기능

현재 구현한 기능은 다음과 같다.

* `.env`에서 Notion Integration Token과 API 버전을 읽는다.
* Notion 페이지의 Markdown 조회 가능 여부를 확인한다.
* 로컬 Markdown 파일을 읽어 Notion 페이지 내용으로 교체한다.
* `config/pages.json`에 등록한 페이지 키로 동기화 대상을 선택한다.
* `config/pages.json`에 등록한 모든 페이지를 한 번에 동기화한다.
* `--dry-run` 옵션으로 실제 수정 없이 동기화 대상을 확인한다.
* 동기화 전 기존 Notion 페이지 Markdown을 `backup/`에 저장한다.
* Notion API의 일시적인 제한이나 서버 오류가 발생하면 짧게 재시도한다.

추가로 고려하는 기능은 다음과 같다.

* Markdown 변경 감지 후 자동 동기화
* GitHub Actions 기반 자동 실행
* 실행 로그와 실패 케이스 정리

## 기술 스택

* Python
* Notion API
* Markdown
* requests
* python-dotenv
* Git / GitHub

## 프로젝트 구조

```text
notion-note-sync/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── config/
│   ├── pages.example.json
│   └── pages.json
├── notes/
│   └── sample.md
├── notionkit/
│   ├── __init__.py
│   ├── client.py
│   └── settings.py
└── scripts/
    ├── check_connection.py
    └── sync_page.py
```

`config/pages.json`과 `.env`는 로컬 전용 파일이다. 실제 토큰이나 개인 Page ID가 들어갈 수 있으므로 Git에 올리지 않는다.

## 환경 설정

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

Notion API 버전은 Notion에서 허용하는 날짜 값이어야 한다. 잘못된 버전을 넣으면 `missing_version` 오류가 발생한다.

## 설치

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

## Notion 페이지 연결

Notion Integration을 만든 뒤, 동기화할 Notion 페이지에 해당 Integration을 연결해야 한다.

페이지가 Integration에 공유되지 않으면 API 요청은 404로 실패한다. 이때 응답에는 보통 `object_not_found`와 함께 페이지를 Integration에 공유하라는 메시지가 나온다.

확인 순서는 다음과 같다.

1. Notion에서 대상 페이지를 연다.
2. 오른쪽 위 `Share` 또는 `...` 메뉴를 연다.
3. `Connections`에서 이 프로젝트의 Integration을 추가한다.
4. Page ID를 `config/pages.json`에 저장한다.

## 페이지 매핑 설정

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

## 연결 테스트

Notion 페이지 접근 권한과 Markdown 조회 가능 여부를 확인한다.

```powershell
python scripts\check_connection.py --page-id "NOTION_PAGE_ID"
```

정상 연결되면 페이지 ID, Markdown 길이, 일부 미리보기 내용이 출력된다.

## 동기화 실행

설정 파일에 등록한 페이지 키로 실행한다.

```powershell
python scripts\sync_page.py --page sample
```

설정 파일에 등록한 모든 페이지를 실행하려면 `--all`을 사용한다.

```powershell
python scripts\sync_page.py --all
```

실제 Notion 페이지를 수정하지 않고 대상만 확인하려면 `--dry-run`을 사용한다.

```powershell
python scripts\sync_page.py --page sample --dry-run
```

전체 동기화도 dry-run으로 먼저 확인할 수 있다.

```powershell
python scripts\sync_page.py --all --dry-run
```

Page ID와 Markdown 파일을 직접 지정할 수도 있다.

```powershell
python scripts\sync_page.py --page-id "NOTION_PAGE_ID" --file "notes/sample.md"
```

기본 동기화는 Notion 페이지를 교체하기 전에 기존 Markdown을 `backup/` 디렉터리에 저장한다. 백업 파일 이름에는 실행 시각, 페이지 제목, Page ID 앞 8자리가 포함된다.

백업 위치를 바꾸려면 `--backup-dir`을 사용한다.

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

## 보안 원칙

이 프로젝트는 나중에 공개 저장소로 전환할 가능성을 고려한다. 그래서 민감한 정보는 처음부터 분리해서 관리한다.

* `.env`에는 실제 Notion API Token만 저장한다.
* `.env`는 Git에 커밋하지 않는다.
* 실제 Notion Page ID는 `config/pages.json`에 저장한다.
* 공개 저장소에는 `config/pages.example.json`만 포함한다.
* 개인 노트나 민감한 자료는 `notes/private/`에 두고 커밋하지 않는다.
* 공개 전에는 Git 히스토리에 토큰이나 개인 Page ID가 남아 있지 않은지 확인한다.

## 커밋 메시지 규칙

이 프로젝트는 Conventional Commits 형식을 참고한다.

```text
type(scope): description
```

예시는 다음과 같다.

```text
init: create base project directories
docs(readme): add project documentation
config(gitignore): ignore local environment and private files
config(env): add example environment variables
config(notion): add example page mapping
feat(sync): implement markdown page sync command
fix(auth): handle missing notion token
refactor(client): extract notion api request logic
test(sync): add sync page test cases
chore(deps): update dependencies
```

자주 쓰는 타입은 다음과 같다.

| Type | 의미 |
| --- | --- |
| `init` | 프로젝트 초기 구조 생성 |
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 수정 |
| `style` | 코드 포맷, 공백, 세미콜론 등 비동작 변경 |
| `refactor` | 기능 변화 없는 코드 구조 개선 |
| `test` | 테스트 추가 또는 수정 |
| `chore` | 패키지, 빌드, 기타 관리 작업 |
| `config` | 환경 설정 파일 수정 |
| `security` | 보안 관련 수정 |

## 개발 로드맵

### Phase 1. Repository Setup

* 기본 디렉터리 구조 생성
* `.gitignore` 작성
* `.env.example` 작성
* `requirements.txt` 작성
* README 작성

### Phase 2. Notion API Connection

* Notion Integration 생성
* 환경 변수 기반 인증 처리
* Notion API 요청 테스트
* 페이지 접근 권한 확인

### Phase 3. Markdown Sync

* Markdown 파일 읽기
* Notion 페이지에 Markdown 내용 반영
* 페이지 매핑 설정 적용
* 단일 페이지 동기화 명령 구현
* 동기화 전 기존 페이지 Markdown 백업

### Phase 4. Multi Page Sync

* 여러 페이지 일괄 동기화
* 동기화 대상 설정 파일 관리
* 실행 로그 출력
* 실패 케이스 예외 처리

### Phase 5. Portfolio Ready

* 예제 문서 추가
* 사용법 정리
* 보안 점검
* 공개 저장소 전환 준비

## 공개 전 체크리스트

공개 저장소로 전환하기 전에 다음 항목을 확인한다.

* `.env`가 커밋되지 않았는가
* 실제 Notion Token이 Git 히스토리에 남아 있지 않은가
* 실제 개인 Notion Page ID가 공개 파일에 포함되지 않았는가
* 개인 강의자료, PDF, 원문 자료가 포함되지 않았는가
* README만 보고 프로젝트 목적과 실행 방법을 이해할 수 있는가
* 실행 가능한 예제 파일이 포함되어 있는가
* 커밋 메시지 히스토리가 일관적인가

## License

초기 개발 단계에서는 라이선스를 지정하지 않는다.

공개 저장소로 전환하기 전에 공개 범위와 사용 목적에 맞는 라이선스를 선택할 예정이다.
