from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


@app.get("/")
def index(request: Request):
    tasks = load_tasks()
    # Render template manually to avoid Jinja2 cache KeyError when context contains
    # unhashable values (like Request objects) which break Jinja2's template cache key.
    template = templates.env.get_template("index.html")
    content = template.render(request=request, tasks=tasks)
    return HTMLResponse(content)


@app.post("/add")
async def add(text: str = Form(...)):
    tasks = load_tasks()
    task = {"id": next_id(tasks), "text": text.strip(), "done": False}
    tasks.append(task)
    save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle/{task_id}")
def toggle(task_id: int):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{task_id}")
def delete(task_id: int):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)
