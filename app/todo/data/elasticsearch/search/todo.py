from typing import List
from todo.data.elasticsearch.documents.todo import TodoIndex
from todo.data.models.todo import Todo, TodoList

def search_todos(query: str) -> List[TodoIndex]:
    return TodoIndex.search().query("match", title=query).execute()

def index_todo_list(todo_list: TodoList) -> None:
    for todo in todo_list.todos:
        index_todo(todo)

def index_todo(todo: Todo) -> None:

    todo_document = TodoIndex(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        list_id=todo.list_id
    )
    todo_document.save()

def update_indexed_todo(todo: Todo) -> None:
    todo_document = TodoIndex.get(id=todo.id)
    todo_document.title = todo.title
    todo_document.description = todo.description
    todo_document.due_date = todo.due_date
    todo_document.list_id = todo.list_id
    todo_document.save()

def delete_indexed_todo(todo_id: int) -> None:
    TodoIndex.delete(id=todo_id)
