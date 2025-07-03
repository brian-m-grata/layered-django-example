from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TodoListQueryParams(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    name: Optional[str] = None

class TodoQueryParams(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None

class TodoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    list_id: Optional[int] = None


class TodoListBase(BaseModel):
    name:  Optional[str] = None


class TodoCreate(TodoBase):
    title: str
    list_id: int
    description: Optional[str] = ""
    due_date: Optional[str] = Field(default_factory=lambda: datetime.now().date().isoformat())


class TodoUpdate(TodoBase):
    pass


class TodoListCreate(TodoListBase):
    name: str


class TodoListUpdate(TodoListBase):
    pass

class TodoListResponse(TodoListBase):
    id: int
    todos: List[TodoBase] = []

class TodoResponse(TodoBase):
    id: int
