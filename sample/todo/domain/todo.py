from typing import List
from pydantic import BaseModel
from django.db.models import Model

from todo.data.models.todo import TodoList, Todo
from todo.interfaces.schema.todo import TodoListCreate, TodoListUpdate, TodoCreate, TodoUpdate
from todo.data.elasticsearch.search.todo import delete_indexed_todo, update_indexed_todo, index_todo


def _update_model(model: Model, data: BaseModel) -> Model:
    for k, v in data.dict().items():
        if hasattr(model, k):
            setattr(model, k, v)
    return model


def create_todo_list(todo_list_in: TodoListCreate) -> TodoList:
    todo_list = TodoList(name=todo_list_in.name)
    todo_list.save()
    return todo_list


def update_todo_list(todo_list_in: TodoListUpdate) -> TodoList:
    todo_list = TodoList.objects.filter(id=todo_list_in.id).first()
    if not todo_list:
        raise ValueError("Todo list not found")
    _update_model(todo_list, todo_list_in)
    todo_list.save()
    return todo_list


def delete_todo_list(todo_list_id: int) -> None:
    todo_list = TodoList.objects.filter(id=todo_list_id).first()
    if not todo_list:
        raise ValueError("Todo list not found")
    todo_list.delete()
    return None


def list_todo_lists() -> List[TodoList]:
    return TodoList.objects.all()


def get_todo_list(todo_list_id: int) -> TodoList:
    todo_list = TodoList.objects.filter(id=todo_list_id).first()
    if not todo_list:
        raise ValueError("Todo list not found")
    return todo_list


def get_todo_list_todos(todo_list_id: int) -> List[Todo]:
    todo_list = TodoList.objects.filter(id=todo_list_id).first()
    if not todo_list:
        raise ValueError("Todo list not found")
    return todo_list.todos


def get_todo(todo_list_id: int, todo_id: int) -> Todo:
    todo = Todo.objects.filter(id=todo_id, list_id=todo_list_id).first()
    if not todo:
        raise ValueError("Todo not found")
    return todo


def create_todo(todo_in: TodoCreate) -> Todo:
    todo_list = get_todo_list(todo_in.list_id)
    todo = Todo(title=todo_in.title, description=todo_in.description, due_date=todo_in.due_date, list=todo_list)
    todo.save()

    # index the todo in elasticsearch instead of adding it to Todo.save()
    # index_todo(todo)

    return todo


def update_todo(todo_id: int, todo_in: TodoUpdate) -> Todo:
    todo = get_todo(todo_in.list_id, todo_id)
    _update_model(todo, todo_in)
    todo.save()

    # index the todo in elasticsearch instead of adding it to Todo.save()
    # update_indexed_todo(todo)

    return todo


def delete_todo(todo_list_id: int, todo_id: int) -> None:
    todo = get_todo(todo_list_id, todo_id)
    todo.delete()

    # delete the todo from elasticsearch instead of adding it to Todo.delete()
    # delete_indexed_todo(todo_id)

    return None
