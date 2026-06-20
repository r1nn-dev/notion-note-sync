# Project Status

## 현재 구현된 기능

| 영역 | 상태 |
| --- | --- |
| 환경 변수 로딩 | `.env`에서 `NOTION_TOKEN`, `NOTION_VERSION` 로드 |
| 연결 확인 | `check_connection.py`로 Page Markdown 조회 테스트 |
| 단일 페이지 동기화 | `--page` 또는 `--page-id`/`--file`로 실행 |
| 전체 페이지 동기화 | `--all`로 `config/pages.json` 전체 실행 |
| dry-run | `--dry-run`으로 Notion 수정 없이 대상 확인 |
| 백업 | 동기화 전 기존 Notion Markdown을 `backup/`에 저장 |
| 백업 제어 | `--backup-dir`, `--skip-backup` 지원 |
| 로그 파일 | `--log-file`로 콘솔 출력과 오류를 파일에 저장 |
| 실패 요약 | 전체 동기화 종료 시 성공/실패 개수와 실패 상세 출력 |
| API 재시도 | 429, 500, 503, 504, 529 응답에 대해 재시도 |
| 설정 검증 | `config/pages.json` 구조와 필수 값 검증 |
| 보안 점검 | `check_public_ready.py`로 민감 정보 포함 여부 점검 |
| 테스트 | `pytest` 단위 테스트 포함 |

## 아직 구현하지 않은 기능

| 기능 | 설명 |
| --- | --- |
| 변경 감지 동기화 | 수정된 Markdown 파일만 골라 동기화 |
| watch 모드 | 파일 변경을 감시하다가 자동 동기화 |
| GitHub Actions 실행 | 원격 저장소 push 또는 schedule 기반 자동 실행 |
| 양방향 동기화 | Notion 변경 내용을 로컬 Markdown으로 가져오기 |
| Markdown diff 출력 | 동기화 전 변경 차이 확인 |

## 현재 사용 권장 흐름

1. `notes/` 아래 Markdown 파일을 수정한다.
2. `python scripts\sync_page.py --page PAGE_KEY --dry-run`으로 대상과 파일을 확인한다.
3. `python scripts\sync_page.py --page PAGE_KEY`로 동기화한다.
4. 필요한 경우 `backup/`에서 이전 Notion Markdown을 확인한다.
5. 여러 페이지는 `python scripts\sync_page.py --all --dry-run` 후 `python scripts\sync_page.py --all`로 실행한다.

## License

현재 별도 라이선스를 지정하지 않는다.
