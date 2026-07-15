from sqlalchemy.orm import Session
from . import models


def get_todos(db: Session, status: str = "all"):
    query = db.query(models.Todo)
    if status == "active":
        query = query.filter(models.Todo.completed.is_(False))
    elif status == "completed":
        query = query.filter(models.Todo.completed.is_(True))
    return query.order_by(models.Todo.created_at.desc()).all()


def create_todo(db: Session, title: str):
    todo = models.Todo(title=title, completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def toggle_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return todo


def count_active_todos(db: Session):
    return db.query(models.Todo).filter(models.Todo.completed.is_(False)).count()
