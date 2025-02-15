from celery import shared_task

from todo.application.use_cases.upload_todo_list import UploadTodoListUseCase


@shared_task
def add_todo_list_from_csv(*args, **kwargs) -> None:
    todo_list_name = kwargs.get("todo_list_name")
    if not todo_list_name:
        raise ValueError("todo_list_name is required")

    todo_list_file_name = kwargs.get("todo_list_file_name")
    if not todo_list_file_name:
        raise ValueError("todo_list_file_name is required")

    UploadTodoListUseCase(todo_list_name, todo_list_file_name).execute()