from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    completed: bool


class Todo(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
