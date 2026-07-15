# 구현 계획: 오늘의 할 일 웹 앱

**브랜치**: `001-todo-app`  
**작성일**: 2026-07-15  
**스펙**: [spec.md](../spec.md)

## 요약

이 기능은 FastAPI 기반의 단일 사용자 할 일 관리 웹 앱으로, REST API와 서버 렌더링 화면을 함께 제공한다. 사용자는 할 일을 생성·완료 토글·삭제할 수 있고, 필터와 남은 개수, 빈 상태, 반응형 화면을 통해 목록을 관리할 수 있다.

## 기술 컨텍스트

- 언어/버전: Python 3.11+
- 주요 의존성: FastAPI, SQLAlchemy 2.x, Pydantic, pytest, httpx/FastAPI TestClient
- 저장소: SQLite, 경로는 .env의 DATABASE_URL로 관리
- 테스트: pytest + FastAPI TestClient
- 대상 플랫폼: 웹 브라우저
- 프로젝트 유형: 웹 애플리케이션
- 성능 목표: 단일 사용자 기준으로 동시 요청 수가 많지 않음
- 제약 조건: 별도 빌드 도구 없이 구현, 단일 페이지 화면 사용
- 범위/규모: 기본 할 일 관리 기능 중심

## Constitution Check

- 모든 산출 문서는 한국어로 작성한다.
- 핵심 기능은 테스트가 먼저 정의되고, 구현 완료 전 테스트가 통과해야 한다.
- 환경 설정은 .env와 .env.example로 관리한다.
- 커밋 메시지는 태스크 ID를 포함해야 한다.

## 프로젝트 구조

```text
app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
└── templates/
    └── index.html

tests/
└── test_api.py
```

## 구현 접근 방식

1. SQLite 연결과 세션 관리 모듈을 구성한다.
2. Todo ORM 모델과 Pydantic 스키마를 정의한다.
3. CRUD 로직을 분리해 API 엔드포인트와 화면 동작을 연결한다.
4. Jinja2 템플릿과 바닐라 JavaScript fetch를 사용해 페이지 새로고침 없이 목록을 갱신한다.
5. pytest 기반 API 테스트를 작성하고, 기능이 통과할 때까지 반복 수정한다.

## 작업 단계

### Phase 1: 기반 구조
- app/database.py를 통해 SQLite 연결 설정
- app/models.py에 Todo 모델 정의
- app/schemas.py에 요청/응답 스키마 정의
- app/crud.py에 생성/조회/수정/삭제 로직 구현

### Phase 2: API 및 화면
- app/main.py에 REST 라우터 구현
- app/templates/index.html에 UI와 fetch 기반 상호작용 구현
- /, /api/todos, /api/todos/{id}, /health 엔드포인트 연결

### Phase 3: 테스트 및 검증
- tests/test_api.py에 생성/완료 토글/삭제/필터/남은 개수 테스트 작성
- 빈 제목, 길이 초과, 삭제 실패 케이스 검증
- 반응형 화면과 빈 상태는 UI 수준 검증을 포함할 수 있음

## 리스크와 대응

- SQLite 경로가 .env 설정과 일치하지 않을 수 있으므로 환경 변수 로딩 방식을 명확히 한다.
- Jinja2 템플릿과 fetch 기반 렌더링이 동시에 동작할 경우 상태 동기화가 불안정할 수 있으므로 단일 데이터 갱신 흐름으로 통일한다.
- API 응답 포맷이 UI와 다르게 되지 않도록 스키마를 먼저 정의한다.
