# Notion Note Sync

Markdown 기반 학습 노트를 Notion 페이지에 자동 반영하기 위한 Python 자동화 프로젝트입니다.

이 프로젝트는 강의 노트, 개인 학습 정리, 기술 문서 초안을 Markdown으로 관리하고, Notion API를 통해 지정된 Notion 페이지에 동기화하는 것을 목표로 합니다.

## 1. 프로젝트 목적

Notion은 학습 노트와 문서 정리에 편리하지만, 긴 Markdown 정리본을 매번 수동으로 복사하거나 파일로 업로드하는 과정은 비효율적입니다.

이 프로젝트는 Markdown 기반 문서 작성 흐름을 Notion과 연결하여 반복적인 수동 편집 작업을 줄이는 것을 목표로 합니다.

주요 목표는 다음과 같습니다.

* Markdown 파일을 Notion 페이지에 자동 반영
* Notion API 기반 문서 업데이트 자동화
* 개인 학습 노트와 기술 문서의 버전 관리
* 민감한 설정 파일과 공개 가능한 예시 파일 분리
* 추후 Public Repository 전환을 고려한 포트폴리오형 프로젝트 구성

## 2. 문제 정의

기존 Notion 기반 노트 정리 방식에는 다음과 같은 문제가 있습니다.

* 긴 학습 노트를 매번 수동으로 붙여넣어야 함
* 여러 Notion 페이지를 일관된 형식으로 관리하기 어려움
* Markdown 파일과 Notion 페이지의 버전 관리가 분리됨
* API Token, Page ID 등 민감한 설정을 안전하게 관리해야 함
* 나중에 포트폴리오로 공개하기 위해 코드와 개인 데이터를 분리해야 함

## 3. 핵심 기능

현재 목표 기능은 다음과 같습니다.

* Markdown 파일 읽기
* Notion API 인증 처리
* 특정 Notion 페이지에 Markdown 내용 반영
* 챕터별 Notion 페이지 매핑 관리
* 공개 가능한 예시 설정과 비공개 로컬 설정 분리

향후 확장 기능은 다음과 같습니다.

* 여러 Notion 페이지 일괄 동기화
* 기존 Notion 페이지 내용 백업
* Markdown 변경 감지 후 자동 동기화
* GitHub Actions 기반 자동 실행
* Notion MCP 또는 LLM 기반 문서 보정 워크플로우 연동

## 4. 기술 스택

* Python
* Notion API
* Markdown
* requests
* python-dotenv
* Git / GitHub

## 5. 프로젝트 구조

```text
notion-note-sync/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── config/
│   └── pages.example.json
├── notes/
│   └── sample.md
└── scripts/
    └── .gitkeep
```

## 6. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```

Windows PowerShell에서는 다음 명령어를 사용할 수 있습니다.

```powershell
Copy-Item .env.example .env
```

`.env` 파일에 실제 Notion Integration Token을 입력합니다.

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_VERSION=2026-03-11
```

주의: `.env` 파일은 절대 GitHub에 커밋하지 않습니다.

## 7. 설치 방법

가상환경을 생성합니다.

```bash
python -m venv .venv
```

가상환경을 활성화합니다.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 8. 사용 예시

현재는 프로젝트 초기 세팅 단계입니다.

향후 목표 실행 명령어는 다음과 같습니다.

```bash
python scripts/sync_page.py --page sample
```

또는 특정 Markdown 파일과 Notion Page ID를 직접 지정하는 방식도 지원할 예정입니다.

```bash
python scripts/sync_page.py --page-id "NOTION_PAGE_ID" --file "notes/sample.md"
```

## 9. 보안 원칙

이 프로젝트는 추후 Public Repository로 공개될 수 있으므로 다음 원칙을 따릅니다.

* 실제 Notion API Token은 `.env`에만 저장합니다.
* `.env` 파일은 Git에 커밋하지 않습니다.
* 실제 Notion Page ID는 `config/pages.json`에 저장합니다.
* 공개 레포에는 `config/pages.example.json`만 포함합니다.
* 개인 학습 노트 원문이나 민감한 자료는 `notes/private/`에 보관하고 커밋하지 않습니다.
* Public 전환 전 Git 히스토리에 민감정보가 포함되어 있지 않은지 확인합니다.

## 10. 커밋 메시지 규칙

이 프로젝트는 Conventional Commits 스타일을 참고합니다.

커밋 메시지 형식은 다음과 같습니다.

```text
type(scope): description
```

예시:

```text
init: create base project directories
docs(readme): add project documentation
config(gitignore): ignore local environment and private files
config(env): add example environment variables
feat(sync): implement markdown page sync command
fix(auth): handle missing notion token
refactor(client): extract notion api request logic
test(sync): add sync page test cases
chore(deps): update dependencies
```

### Commit Type

| Type       | 의미                  |
| ---------- | ------------------- |
| `init`     | 프로젝트 초기 구조 생성       |
| `feat`     | 새로운 기능 추가           |
| `fix`      | 버그 수정               |
| `docs`     | 문서 수정               |
| `style`    | 코드 포맷팅, 공백, 세미콜론 등  |
| `refactor` | 기능 변화 없는 코드 구조 개선   |
| `test`     | 테스트 코드 추가 또는 수정     |
| `chore`    | 패키지, 설정, 빌드 등 기타 작업 |
| `config`   | 환경설정 파일 수정          |
| `security` | 보안 관련 수정            |

### Commit Message Examples

```text
init: create base project directories
docs(readme): add project documentation
config(gitignore): ignore local environment and private files
config(env): add example environment variables
config(notion): add example page mapping
chore(deps): add initial Python dependencies
docs(sample): add sample markdown note
feat(sync): implement markdown page sync command
fix(sync): handle invalid page mapping key
refactor(client): extract notion api request logic
```

## 11. 개발 로드맵

### Phase 1. Repository Setup

* GitHub Private Repository 생성
* 기본 폴더 구조 생성
* `.gitignore` 작성
* `.env.example` 작성
* `requirements.txt` 작성
* README 작성

### Phase 2. Notion API Connection

* Notion Integration 생성
* 환경변수 기반 인증 처리
* Notion API 요청 테스트
* Notion 페이지 권한 연결

### Phase 3. Markdown Sync

* Markdown 파일 읽기
* Notion 페이지에 Markdown 내용 반영
* 페이지 매핑 설정 적용
* 단일 페이지 동기화 명령어 구현

### Phase 4. Multi Page Sync

* 여러 페이지 일괄 동기화
* 동기화 대상 설정 파일 관리
* 실행 로그 출력
* 실패 케이스 예외 처리

### Phase 5. Portfolio Ready

* 예제 문서 추가
* 사용법 정리
* 보안 점검
* Public Repository 전환 준비

## 12. 공개 전 체크리스트

Public Repository로 전환하기 전에 다음 항목을 확인합니다.

* `.env` 파일이 커밋되지 않았는가?
* 실제 Notion Token이 Git 히스토리에 남아 있지 않은가?
* 실제 개인 Notion Page ID가 공개 파일에 포함되지 않았는가?
* 개인 강의자료, PDF, 대본 원문이 포함되지 않았는가?
* README만 보고 프로젝트 목적과 사용법을 이해할 수 있는가?
* 실행 가능한 예제 파일이 포함되어 있는가?
* 커밋 메시지 히스토리가 일관적인가?

## 13. License

초기 개발 단계에서는 라이선스를 지정하지 않습니다.

Public Repository로 전환하기 전에 공개 범위와 재사용 정책에 맞는 라이선스를 선택할 예정입니다.
