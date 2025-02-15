
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from todo.models import Todo, TodoList
from todo.interfaces.schema.todo import TodoCreate, TodoUpdate, TodoList, TodoListCreate, TodoListUpdate, TodoResponse, TodoListResponse
from todo.services.todo import (
    create_todo_list, 
    create_todo, 
    update_todo, 
    delete_todo, 
    get_todo_list, 
    get_todo_list_todos, 
    list_todo_lists, 
    update_todo_list
)

# Create your views here.
class ListTodoListsView(APIView):

    def get(self, request: Request, *args, **kwargs):

        # can add params to filter and pagination into the service
        todo_lists = list_todo_lists()

        response_body = [TodoListResponse(**todo_list.dict()) for todo_list in todo_lists]

        return Response({"results": response_body}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        
        todo_list_in = TodoListCreate(**request.data)

        todo_list = create_todo_list(todo_list_in)

        response_body = TodoListResponse(**todo_list.dict())

        return Response(response_body.dict(), status=status.HTTP_201_CREATED)

class SingleTodoListView(APIView):

    def get(self, request: Request, todo_list_id: int, *args, **kwargs):

        todo_list = get_todo_list(todo_list_id)

        response_body = TodoListResponse(**todo_list.dict())

        return Response(response_body.dict(), status=status.HTTP_200_OK)

    def patch(self, request: Request, todo_list_id: int, *args, **kwargs):

        todo_list_in = TodoListUpdate(**request.data)

        todo_list = update_todo_list(todo_list_id, todo_list_in)

        response_body = TodoListResponse(**todo_list.dict())

        return Response(response_body.dict(), status=status.HTTP_200_OK)

    def delete(self, request: Request, todo_list_id: int, *args, **kwargs):

        todo_list = TodoList.objects.filter(id=todo_list_id).first()

        if todo_list:
            todo_list.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ListTodoView(APIView):
    def get(self, request: Request, list_id: int, *args, **kwargs):

        todos = get_todo_list_todos(list_id)

        response_body = [TodoResponse(**todo.dict()) for todo in todos]

        return Response(response_body.dict(), status=status.HTTP_200_OK)


    def post(self, request: Request, list_id: int, *args, **kwargs):
        
        todo_in = TodoCreate(list_id=list_id, **request.data)

        todo = create_todo(todo_in)

        response_body = TodoResponse(**todo.dict())

        return Response(response_body.dict(), status=status.HTTP_201_CREATED)

class SingleTodoView(APIView):

    def get(self, request: Request, list_id: int, todo_id: int, *args, **kwargs):
        pass

    def patch(self, request: Request, list_id: int, todo_id: int, *args, **kwargs):
        todo = Todo.objects.filter(id=todo_id).first()

        if not todo:
            raise NotFound(detail=f"Todo {todo_id} not found.")

        for k, v in request.data.items():
            if hasattr(todo, k, None):
                setattr(todo, k, v)

        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request: Request, todo_id: int, *args, **kwargs):
        todo = Todo.objects.filter(id=todo_id).first()

        if not todo:
            raise NotFound(detail=f"Todo {todo_id} not found.")

        todo.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)