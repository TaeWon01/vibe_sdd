# 연구 결과: 오늘의 할 일 웹 앱

## 결정 사항

- 백엔드는 Python 3.11+ 환경에서 FastAPI를 사용한다.
- 데이터베이스는 SQLite를 사용하고, 파일 경로는 .env의 DATABASE_URL 환경변수로 관리한다.
- 프론트엔드는 단일 index.html 기반의 Jinja2 템플릿과 바닐라 JavaScript fetch를 사용한다.
- 테스트는 pytest와 FastAPI TestClient를 사용해 API 동작을 검증한다.
- API는 REST 스타일로 설계하고, 목록 조회/생성/수정/삭제/상태 확인 엔드포인트를 제공한다.

## 근거

- FastAPI는 기존 프로젝트의 Python 기반 구조와 잘 맞고, API와 템플릿 기반 화면을 함께 구현하기에 적합하다.
- SQLite는 초기 구현과 데이터 영속성 요구를 만족하면서 설정이 단순하다.
- Jinja2 템플릿과 바닐라 JavaScript를 조합하면 별도 빌드 도구 없이 빠르게 구현할 수 있다.
- pytest와 TestClient 조합은 API 중심 기능의 회귀 테스트를 효율적으로 수행할 수 있다.

## 대안 검토

- PostgreSQL: 기능상 충분하지만 현재 범위와 설정 복잡도를 고려하면 과다하다.
- React/Vue 같은 SPA 프레임워크: 별도 빌드 파이프라인이 필요해 현재 요구사항에 비해 과하다.
- 단일 파일 Flask 스타일 구현: 빠르지만 구조 확장성과 테스트 가능성이 떨어진다.
