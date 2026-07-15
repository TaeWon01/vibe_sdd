from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import crud, schemas, models

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/todos", response_model=list[schemas.Todo])
def list_todos(status: str = "all", db: Session = Depends(get_db)):
    return crud.get_todos(db, status=status)


@app.post("/api/todos", response_model=schemas.Todo, status_code=201)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title is required")
    if len(title) > 100:
        raise HTTPException(status_code=422, detail="Title must be 100 characters or less")
    return crud.create_todo(db, title)


@app.patch("/api/todos/{todo_id}", response_model=schemas.Todo)
def toggle_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.toggle_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/api/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
