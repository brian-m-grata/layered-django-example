
from django.urls import path
from todo.interfaces.views.todo import (
    ListTodoView,
    ListTodoListsView,
    SingleTodoListView,
    SingleTodoView
)

urlpatterns = [
    path("/todo_lists", ListTodoListsView.as_view()),
    path("/todo_lists/<int:todo_list_id>/", SingleTodoListView.as_view()),
    path("/todo_lists/<int:todo_list_id>/todos", ListTodoView.as_view()),
    path("/todo_lists/<int:todo_list_id>/todos/<int:todo_id>", SingleTodoView.as_view())
]