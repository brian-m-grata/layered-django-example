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

## 🚀 Setup and Installation

### Prerequisites
- Python 3.10+
- Poetry (dependency management)
- PostgreSQL
- Redis
- Elasticsearch (optional, for search functionality)

### Installation

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database and service configurations
   ```

3. **Database setup**
   ```bash
   poetry run python manage.py migrate
   poetry run python manage.py createsuperuser
   ```

4. **Start the application**
   ```bash
   poetry run python manage.py runserver
   ```

5. **Start Celery worker (in another terminal)**
   ```bash
   poetry run celery -A sample.celery_app worker --loglevel=info
   ```

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
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the new feature",
    "due_date": "2024-01-20",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
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

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the sample directory:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=password
POSTGRES_NAME=app

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Elasticsearch Configuration (optional)
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings

Key settings in `sample/settings.py`:

```python
# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": POSTGRES_HOST,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "PORT": POSTGRES_PORT,
        "NAME": POSTGRES_NAME
    }
}

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
poetry run python manage.py test

# Run specific test file
poetry run python manage.py test todo.tests

# Run with coverage
poetry run coverage run --source='.' manage.py test
poetry run coverage report
poetry run coverage html  # Generate HTML report
```

### Test Structure
Tests follow the same layered architecture:

```
todo/
├── tests/
│   ├── test_domain.py      # Domain layer tests
│   ├── test_application.py # Application layer tests
│   ├── test_data.py        # Data layer tests
│   └── test_interfaces.py  # Interface layer tests
```

## 🔍 Search Functionality

The application includes Elasticsearch integration for advanced search capabilities:

```python
# Search todos by title or description
from todo.data.elasticsearch.search.todo import search_todos

results = search_todos("project documentation")
```

## 📦 Dependencies

### Core Dependencies
- **Django 5.1**: Web framework
- **Django REST Framework**: API framework
- **Pydantic**: Data validation and serialization
- **psycopg2-binary**: PostgreSQL adapter
- **celery**: Background task processing
- **redis**: Message broker and caching
- **elasticsearch-dsl**: Elasticsearch integration

### Development Dependencies
- **poetry**: Dependency management
- **coverage**: Test coverage reporting
- **pytest**: Testing framework (optional)

## 🚀 Deployment

### Docker Deployment
The application is containerized and can be deployed using Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Production Considerations
1. Set `DEBUG=False` in production
2. Use environment variables for sensitive configuration
3. Configure proper database backups
4. Set up monitoring and logging
5. Use a production-grade WSGI server (Gunicorn)
6. Configure reverse proxy (Nginx)

## 🤝 Contributing

When contributing to this project:

1. Follow the Clean Architecture principles
2. Add tests for new functionality
3. Update documentation for API changes
4. Use Pydantic schemas for input validation
5. Follow Django coding standards
6. Ensure all layers remain properly separated

## 📖 Additional Resources

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
