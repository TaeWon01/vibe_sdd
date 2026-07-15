# Todo API 계약서

## 공통 사항

- 모든 응답은 JSON 형식으로 반환한다.
- 오류 응답은 적절한 HTTP 상태 코드와 에러 메시지를 포함한다.

## 엔드포인트

### GET /api/todos
- 설명: 할 일 목록을 조회한다.
- 쿼리 파라미터:
  - status: all | active | completed
- 응답: Todo 목록 배열

### POST /api/todos
- 설명: 새 할 일을 생성한다.
- 요청 본문: { "title": "할 일 제목" }
- 성공 응답: 201 Created
- 실패 응답:
  - 제목이 비어 있거나 공백이면 422 Unprocessable Entity
  - 제목이 100자를 초과하면 422 Unprocessable Entity

### PATCH /api/todos/{id}
- 설명: 할 일 완료 상태를 토글한다.
- 요청 본문: { "completed": true }
- 성공 응답: 업데이트된 Todo 객체
- 실패 응답:
  - 존재하지 않는 id면 404 Not Found

### DELETE /api/todos/{id}
- 설명: 할 일을 삭제한다.
- 실패 응답:
  - 존재하지 않는 id면 404 Not Found

### GET /
- 설명: 메인 화면 HTML을 반환한다.

### GET /health
- 설명: 서비스 상태를 확인한다.
- 응답: { "status": "ok" }
