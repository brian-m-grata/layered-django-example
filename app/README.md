# Django Todo Application

A Django application implementing Clean Architecture principles for managing todo lists and items. This application demonstrates how to structure a Django project with clear separation of concerns and maintainable code.

## 🏗️ Clean Architecture Implementation

This application follows Clean Architecture principles with four distinct layers:

### 1. Domain Layer (`todo/domain/`)
The innermost layer containing pure business logic:

```python
# todo/domain/todo.py
def create_todo_list(todo_list_in: TodoListCreate) -> TodoList:
    todo_list = TodoList(name=todo_list_in.name)
    todo_list.save()
    return todo_list

def create_todo(todo_in: TodoCreate) -> Todo:
    todo_list = get_todo_list(todo_in.list_id)
    todo = Todo(
        title=todo_in.title, 
        description=todo_in.description, 
        due_date=todo_in.due_date, 
        list=todo_list
    )
    todo.save()
    index_todo(todo)  # Integration with Elasticsearch
    return todo
```

**Key Features:**
- Pure business logic with no framework dependencies
- Input validation using Pydantic schemas
- Integration with external services (Elasticsearch)

### 2. Application Layer (`todo/application/`)
Orchestrates use cases and complex workflows:

```python
# todo/application/use_cases/upload_todo_list.py
class UploadTodoListUseCase(UseCase):
    def __init__(self, todo_list_name: str, todo_list_file_name: str) -> None:
        self.todo_list_name = todo_list_name
        self.todo_list_file_name = todo_list_file_name

    def execute(self) -> None:
        todo_list = create_todo_list(self.todo_list_name)
        todo_list_csv_data = read_csv_file(self.todo_list_file_name)
        # Process CSV and create todos...
```

### 3. Data Layer (`todo/data/`)
Handles data persistence and external integrations:

```python
# todo/data/models/todo.py
class TodoList(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Features:**
- Django ORM models
- Elasticsearch integration for search functionality
- Repository pattern implementation

### 4. Interface Layer (`todo/interfaces/`)
Handles external communication and data transformation:

```python
# todo/interfaces/views/todo.py
class ListTodoListsView(APIView):
    def get(self, request: Request, *args, **kwargs):
        # Parse query parameters with Pydantic
        query_params = TodoListQueryParams(**request.GET.dict())
        
        # Call domain function
        todo_lists = list_todo_lists()
        
        # Serialize output
        serializer = TodoListDetailSerializer(todo_lists, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
```

**Features:**
- Django REST Framework views
- Pydantic schemas for input validation
- DRF serializers for output formatting

## 📚 API Documentation

### Todo Lists

#### Get All Todo Lists
```http
GET /api/v1/todo-lists/
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Work Tasks",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "todos_count": 3
    }
  ]
}
```

#### Create Todo List
```http
POST /api/v1/todo-lists/
Content-Type: application/json

{
  "name": "Personal Tasks"
}
```

#### Get Single Todo List
```http
GET /api/v1/todo-lists/{id}/
```

#### Update Todo List
```http
PATCH /api/v1/todo-lists/{id}/
Content-Type: application/json

{
  "name": "Updated List Name"
}
```

#### Delete Todo List
```http
DELETE /api/v1/todo-lists/{id}/
```

### Todos

#### Get Todos in a List
```http
GET /api/v1/todo-lists/{list_id}/todos/
```

**Response:**
```json
{ 
    "results": [
        {
            "id": 1,
            "title": "Complete project documentation",
            "description": "Write comprehensive documentation for the new feature",
            "due_date": "2024-01-20",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Create Todo
```http
POST /api/v1/todo-lists/{list_id}/todos/
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2024-01-25"
}
```

#### Get Single Todo
```http
GET /api/v1/todo-lists/{list_id}/todos/{todo_id}/
```

#### Update Todo
```http
PATCH /api/v1/todo-lists/{list_id}/todos/{todo_id}/
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated description"
}
```

#### Delete Todo
```http
DELETE /api/v1/todo-lists/{list_id}/todos/{todo_id}/
```
