# Security

이 프로젝트는 공개 저장소로 전환할 가능성을 고려해 민감한 정보와 공개 파일을 분리한다.

## Local-Only Files

다음 파일과 디렉터리는 Git에 커밋하지 않는다.

* `.env`
* `.env.*`
* `config/pages.json`
* `notes/private/`
* `backup/`
* `logs/`

예외적으로 `.env.example`은 공개 예시 파일로 커밋한다.

## Public Readiness Check

공개 전에는 다음 명령을 실행한다.

```powershell
python scripts\check_public_ready.py
```

이 스크립트는 Git에 추적 중인 파일을 기준으로 다음 항목을 확인한다.

* 로컬 전용 파일이 추적되고 있지 않은가
* 비공개 노트, 백업, 로그 파일이 추적되고 있지 않은가
* Notion Token처럼 보이는 값이 포함되어 있지 않은가
* 실제 Notion Page ID처럼 보이는 값이 포함되어 있지 않은가

## Public Checklist

공개 저장소로 전환하기 전에 다음 항목을 확인한다.

* `.env`가 커밋되지 않았는가
* 실제 Notion Token이 Git 히스토리에 남아 있지 않은가
* 실제 개인 Notion Page ID가 공개 파일에 포함되지 않았는가
* 개인 강의자료, PDF, 원문 자료가 포함되지 않았는가
* `python scripts\check_public_ready.py`가 통과하는가
* `python -m pytest`가 통과하는가
* README만 보고 프로젝트 목적과 실행 방법을 이해할 수 있는가
* 실행 가능한 예제 파일이 포함되어 있는가
* 커밋 메시지 히스토리가 일관적인가
