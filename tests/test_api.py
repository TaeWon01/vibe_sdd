import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_list_and_create_todo():
    response = client.get('/api/todos')
    assert response.status_code == 200
    assert response.json() == []

    response = client.post('/api/todos', json={'title': '테스트 할 일'})
    assert response.status_code == 201
    assert response.json()['title'] == '테스트 할 일'


def test_validation_and_toggle_and_delete():
    response = client.post('/api/todos', json={'title': ''})
    assert response.status_code == 422

    response = client.post('/api/todos', json={'title': 'x' * 101})
    assert response.status_code == 422

    response = client.post('/api/todos', json={'title': '작업 1'})
    todo_id = response.json()['id']

    response = client.patch(f'/api/todos/{todo_id}', json={'completed': True})
    assert response.status_code == 200
    assert response.json()['completed'] is True

    response = client.delete(f'/api/todos/{todo_id}')
    assert response.status_code == 200

    response = client.delete(f'/api/todos/{todo_id}')
    assert response.status_code == 404


def test_filter_and_remaining_count():
    client.post('/api/todos', json={'title': '첫 번째'})
    client.post('/api/todos', json={'title': '두 번째'})

    response = client.get('/api/todos?status=active')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.patch('/api/todos/1', json={'completed': True})
    assert response.status_code == 200

    response = client.get('/api/todos?status=active')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get('/api/todos?status=completed')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_health_and_template():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

    response = client.get('/')
    assert response.status_code == 200
    assert '오늘의 할 일' in response.text
