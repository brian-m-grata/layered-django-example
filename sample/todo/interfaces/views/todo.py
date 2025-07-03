from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from todo.interfaces.serializers.todo import (
    TodoListSerializer,
    TodoListDetailSerializer,
    TodoSerializer
)
from todo.interfaces.schema.todo import (
    TodoListCreate,
    TodoListUpdate,
    TodoCreate,
    TodoUpdate,
    TodoListQueryParams,
    TodoQueryParams
)
from todo.domain.todo import (
    create_todo_list,
    update_todo_list,
    delete_todo_list,
    list_todo_lists,
    get_todo_list,
    get_todo_list_todos,
    create_todo,
    update_todo,
    delete_todo,
    get_todo
)

# Create your views here.
class ListTodoListsView(APIView):

    def get(self, request: Request, *args, **kwargs):
        # Parse query parameters with Pydantic
        query_params = TodoListQueryParams(**request.GET.dict())
        
        # Call domain function
        todo_lists = list_todo_lists()
        
        # Serialize output
        serializer = TodoListDetailSerializer(todo_lists, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        # Validate input with Pydantic
        try:
            todo_list_data = TodoListCreate(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call domain function
        todo_list = create_todo_list(todo_list_data)
        
        # Serialize output
        serializer = TodoListSerializer(todo_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SingleTodoListView(APIView):

    def get(self, request: Request, list_id: int, *args, **kwargs):
        try:
            # Call domain function
            todo_list = get_todo_list(list_id)
            
            # Serialize output
            serializer = TodoListDetailSerializer(todo_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, list_id: int, *args, **kwargs):
        # Validate input with Pydantic
        try:
            todo_list_data = TodoListUpdate(**request.data)
            todo_list_data.id = list_id  # Set the ID for the domain function
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Call domain function
            todo_list = update_todo_list(todo_list_data)
            
            # Serialize output
            serializer = TodoListSerializer(todo_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, list_id: int, *args, **kwargs):
        try:
            # Call domain function
            delete_todo_list(list_id)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class ListTodoView(APIView):
    def get(self, request: Request, list_id: int, *args, **kwargs):
        # Parse query parameters with Pydantic
        query_params = TodoQueryParams(**request.query_params.dict())
        
        try:
            # Call domain function
            todos = get_todo_list_todos(list_id)
            
            # Serialize output
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request, list_id: int, *args, **kwargs):
        # Validate input with Pydantic
        try:
            todo_data = TodoCreate(list_id=list_id, **request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Call domain function
            todo = create_todo(todo_data)
            
            # Serialize output
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class SingleTodoView(APIView):

    def get(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):
        try:
            # Call domain function
            todo = get_todo(todo_list_id, todo_id)
            
            # Serialize output
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):
        # Validate input with Pydantic
        try:
            data = request.data.copy()
            data['list_id'] = todo_list_id
            todo_data = TodoUpdate(**data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Call domain function
            todo = update_todo(todo_id, todo_data)
            
            # Serialize output
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, todo_list_id: int, todo_id: int, *args, **kwargs):
        try:
            # Call domain function
            delete_todo(todo_list_id, todo_id)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)