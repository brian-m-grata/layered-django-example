from django.urls import path
from todo.interfaces.views.todo import (
    ListTodoView,
    ListTodoListsView,
    SingleTodoListView,
    SingleTodoView
)
from todo.interfaces.views.tasks import (
    process_todo_upload_task,
    cleanup_old_todos_task,
    send_todo_reminders_task,
    get_available_tasks
)

urlpatterns = [
    path("todo-lists/", ListTodoListsView.as_view()),
    path("todo-lists/<int:list_id>/", SingleTodoListView.as_view()),
    path("todo-lists/<int:list_id>/todos/", ListTodoView.as_view()),
    path("todo-lists/<int:list_id>/todos/<int:todo_id>/", SingleTodoView.as_view()),
    
    # Task endpoints
    path("tasks/", get_available_tasks, name="available_tasks"),
    path("tasks/upload/", process_todo_upload_task, name="process_todo_upload"),
    path("tasks/cleanup/", cleanup_old_todos_task, name="cleanup_old_todos"),
    path("tasks/reminders/", send_todo_reminders_task, name="send_todo_reminders"),
]