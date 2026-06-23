# Security

Notion Token, 실제 Page ID, 개인 노트, 백업/로그 파일은 Git에 올리지 않는다.

## Git에 올리지 않는 파일

다음 파일과 디렉터리는 로컬 전용이다.

| 경로 | 이유 |
| --- | --- |
| `.env` | 실제 Notion Integration Token 저장 |
| `.env.*` | 로컬 환경별 토큰이나 설정이 들어갈 수 있음 |
| `config/pages.json` | 실제 Notion Page ID 저장 |
| `notes/private/` | 개인 노트나 비공개 자료 저장 |
| `backup/` | 동기화 전 Notion 페이지 백업 저장 |
| `logs/` | 실행 로그 저장 |

`.env.example`과 `config/pages.example.json`은 예시 파일이므로 Git에 포함한다.

## `.env` 관리

`.env`에는 실제 Notion Token만 둔다.

```env
NOTION_TOKEN=your_actual_token
NOTION_VERSION=2026-03-11
```

주의할 점:

* `.env`를 커밋하지 않는다.
* 토큰을 README, docs, 테스트 파일에 쓰지 않는다.
* 토큰을 터미널 출력이나 로그 파일에 남기지 않는다.
* 토큰이 노출되었다고 판단되면 Notion에서 새 토큰을 발급한다.

## Page ID 관리

실제 Notion Page ID는 `config/pages.json`에만 둔다. 공개 예시에는 더미 값만 사용한다.

```json
{
  "sample": {
    "title": "Sample Notion Page",
    "page_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "file": "notes/sample.md"
  }
}
```

## 백업과 로그

동기화 시 기본적으로 기존 Notion Markdown이 `backup/`에 저장된다. `--log-file`을 사용하면 실행 결과가 `logs/` 같은 경로에 저장될 수 있다.

이 파일들은 실제 문서 내용, 페이지 ID, 실행 경로를 포함할 수 있으므로 Git에 올리지 않는다.

## 민감 정보 점검

현재 Git에 추적 중인 파일을 검사한다.

```powershell
python scripts\check_public_ready.py
```

점검 항목:

* `.env`, `config/pages.json`, `notes/private/`, `backup/`, `logs/`가 추적되고 있지 않은가
* Notion Token처럼 보이는 값이 추적 파일에 들어 있지 않은가
* 실제 Notion Page ID처럼 보이는 값이 추적 파일에 들어 있지 않은가

이 스크립트는 현재 작업트리의 추적 파일을 검사한다. 과거 커밋 히스토리 전체를 보장하지는 않는다.

## 수동 점검 명령

추적 파일 목록 확인:

```powershell
git ls-files
```

작업트리 상태 확인:

```powershell
git status --short
```

현재 추적 파일에서 의심 패턴 검색:

```powershell
git grep -n "secret_"
git grep -n "ntn_"
```

## 커밋 전 체크리스트

* `.env`가 Git 상태에 보이지 않는가
* `config/pages.json`이 Git 상태에 보이지 않는가
* `backup/`과 `logs/`가 Git 상태에 보이지 않는가
* 문서에 실제 토큰이나 실제 Page ID를 쓰지 않았는가
* `python scripts\check_public_ready.py`가 통과하는가
* `python -m pytest`가 통과하는가
