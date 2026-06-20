# Design Notes

이 문서는 `notion-note-sync`의 설계 선택과 제한 사항을 정리한다. 목표는 단순한 자동화 스크립트가 아니라, 권한 범위와 실행 흐름이 명확한 Notion 동기화 도구를 만드는 것이다.

## 문제 정의

Notion은 웹 편집 경험은 좋지만, 반복적으로 작성하는 노트나 학습 기록을 매번 웹에서 수정하기에는 번거롭다. 이 프로젝트는 로컬 Markdown 파일을 기준으로 Notion 페이지를 갱신한다.

핵심 요구사항:

* 로컬 Markdown 파일을 단일 출처로 둔다.
* 동기화 대상 Notion 페이지를 명시적으로 제한한다.
* 실행 전 dry-run으로 어떤 페이지와 파일이 연결되는지 확인한다.
* 동기화 전에 기존 Notion 내용을 백업한다.
* 실패한 페이지와 이유를 확인할 수 있어야 한다.
* 토큰, 실제 Page ID, 개인 노트는 Git에 포함하지 않는다.

## Notion API를 직접 사용하는 이유

이 프로젝트는 MCP 기반 자동화 대신 Notion API를 직접 호출한다.

이유:

* **권한 범위가 명확하다.** Notion Integration이 연결된 페이지에만 접근한다.
* **실행 흐름이 고정되어 있다.** Markdown 읽기, 백업, Notion 교체, 결과 출력 순서가 코드로 정해져 있다.
* **AI에게 쓰기 권한 판단을 넘기지 않는다.** 사용자가 명령을 실행할 때만 Notion 수정이 발생한다.
* **테스트하기 쉽다.** 설정 검증, 재시도, 실패 요약 같은 동작을 단위 테스트로 고정할 수 있다.
* **로그와 백업을 남길 수 있다.** 자동화 결과를 나중에 추적하기 쉽다.

MCP가 적합한 경우도 있다. 예를 들어 AI가 Notion을 탐색하고 대화형으로 수정해야 하는 도구라면 MCP가 더 편하다. 이 프로젝트는 그런 목적이 아니라, 정해진 Markdown 파일을 정해진 Notion 페이지에 반복적으로 반영하는 목적이다.

## 데이터 흐름

```text
notes/*.md
  │
  ▼
scripts/sync_page.py
  │
  ├─ config/pages.json에서 page_id와 file 매핑 로드
  ├─ Markdown 파일 읽기
  ├─ 기존 Notion Markdown 백업
  ├─ Notion API PATCH /v1/pages/{page_id}/markdown
  └─ 성공/실패 결과 출력
```

## 주요 모듈

| 파일 | 역할 |
| --- | --- |
| `notionkit/settings.py` | `.env`에서 Notion 설정 로드 |
| `notionkit/client.py` | Notion Markdown API 요청과 재시도 처리 |
| `scripts/check_connection.py` | Page ID 접근 권한과 Markdown 조회 테스트 |
| `scripts/sync_page.py` | Markdown 파일을 Notion 페이지로 동기화 |
| `scripts/check_public_ready.py` | Git 추적 파일의 민감 정보 점검 |

## 안전장치

| 안전장치 | 설명 |
| --- | --- |
| `--dry-run` | Notion 수정 없이 대상, Page ID, 파일 경로, Markdown 길이 확인 |
| 백업 | 실제 교체 전에 기존 Notion Markdown을 `backup/`에 저장 |
| 설정 검증 | `config/pages.json`의 필수 필드와 JSON 구조 검사 |
| 실패 요약 | 일괄 동기화 시 성공/실패 개수와 실패 이유 출력 |
| API 재시도 | 429, 500, 503, 504, 529 응답에 대해 재시도 |
| 보안 점검 | `.env`, 실제 Page ID, 토큰 패턴이 추적 파일에 들어갔는지 검사 |

## 현재 제한 사항

* Notion 페이지 내용은 Markdown 전체 교체 방식으로 갱신한다.
* 양방향 동기화는 지원하지 않는다.
* Notion에서 수정한 내용을 로컬 Markdown으로 병합하지 않는다.
* Markdown diff 미리보기는 아직 없다.
* 파일 변경 감시나 자동 실행 스케줄은 아직 없다.

## 포트폴리오 관점의 강조점

이 프로젝트에서 보여주려는 것은 단순히 API를 호출하는 코드가 아니다.

* 외부 서비스 권한을 좁게 설계한 점
* 실제 쓰기 동작 전에 확인과 백업을 둔 점
* 실패와 재시도를 운영 관점에서 처리한 점
* 민감 정보가 Git에 들어가지 않도록 점검 스크립트를 둔 점
* CLI 동작을 단위 테스트로 검증한 점
