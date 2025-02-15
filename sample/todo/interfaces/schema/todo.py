from pydantic import BaseModel
from typing import List, Optional


class TodoBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[str]
    list_id: Optional[int]


class TodoListBase(BaseModel):
    name:  Optional[str]


class TodoCreate(TodoBase):
    title: str
    list_id: int


class TodoUpdate(TodoBase):
    pass


class TodoListCreate(TodoList):
    name: str


class TodoListUpdate(TodoList):
    pass

class TodoListResponse(TodoListBase):
    id: int
    todos: List[TodoBase] = []

class TodoResponse(TodoBase):
    id: int
