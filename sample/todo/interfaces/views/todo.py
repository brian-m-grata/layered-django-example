
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from todo.data.models.todo import Todo, TodoList
from todo.interfaces.schema.todo import (
    TodoCreate, 
    TodoListCreate, 
    TodoListUpdate, 
    TodoResponse, 
    TodoListResponse, 
    TodoUpdate, 
    TodoListQueryParams, 
    TodoQueryParams
)  
from todo.domain.todo import (
    create_todo_list, 
    create_todo, 
    update_todo, 
    delete_todo, 
    get_todo_list, 
    get_todo_list_todos, 
    list_todo_lists, 
    update_todo_list,
    get_todo
)

# Create your views here.
class ListTodoListsView(APIView):

    def get(self, request: Request, *args, **kwargs):

        # can add params to filter and pagination into the service
        todo_list_query_params = TodoListQueryParams(**request.GET.data)

        todo_lists = list_todo_lists(**todo_list_query_params.dict())

        response_body = [TodoListResponse(**todo_list.dict()) for todo_list in todo_lists]

        return Response({"results": response_body}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        
        # Validate the request data
        todo_list_in = TodoListCreate(**request.data)

        # Create the todo list
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

        todo_query_params = TodoQueryParams(**request.query_params)

        todos = get_todo_list_todos(list_id, **todo_query_params.dict())

        response_body = [TodoResponse(**todo.dict()) for todo in todos]

        return Response(response_body.dict(), status=status.HTTP_200_OK)


    def post(self, request: Request, list_id: int, *args, **kwargs):
        
        todo_in = TodoCreate(list_id=list_id, **request.data)

        todo = create_todo(todo_in)

        response_body = TodoResponse(**todo.dict())

        return Response(response_body.dict(), status=status.HTTP_201_CREATED)

class SingleTodoView(APIView):

    def get(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):
        todo = get_todo(todo_list_id, todo_id)

        response_body = TodoResponse(**todo.dict())

        return Response(response_body.dict(), status=status.HTTP_200_OK)

    def patch(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):

        todo_in = TodoUpdate(list_id=todo_list_id, **request.data)

        todo = update_todo(todo_id, todo_in)

        response_body = TodoResponse(**todo.dict())

        return Response(response_body.dict(), status=status.HTTP_200_OK)

    def delete(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):
    
        delete_todo(todo_list_id, todo_id)

        return Response(None, status=status.HTTP_204_NO_CONTENT)