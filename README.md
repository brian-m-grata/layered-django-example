# Layered Django Example

A Django application demonstrating Clean Architecture principles with a layered approach to building scalable, maintainable web applications.

## 🏗️ Architecture Overview

This project implements Clean Architecture (also known as Hexagonal Architecture) with clear separation of concerns across multiple layers:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and application services
- **Data Layer**: Data access, models, and external integrations
- **Interface Layer**: Controllers, serializers, and external interfaces

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd layered-django-example
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Django Admin: http://localhost:8000/admin/
   - API Endpoints: http://localhost:8000/api/v1/

### Local Development Setup

1. **Navigate to the app directory**
   ```bash
        cd app
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   poetry run python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   poetry run python manage.py runserver
   ```

## 🚀 Using This Repository as a Template

### Cloning for a New Project

If you want to use this repository as a starting point for your own project:

1. **Clone the repository**
   ```bash
   git clone <repository-url> your-new-project-name
   cd your-new-project-name
   ```

2. **Remove the existing git history and initialize a new repository**
   ```bash
   rm -rf .git
   git init
   ```

3. **Add your new remote repository**
   ```bash
   git remote add origin <your-new-repository-url>
   ```

4. **Make your first commit**
   ```bash
   git add .
   git commit -m "Initial commit: Based on layered Django example"
   git branch -M main
   git push -u origin main
   ```

5. **Update project references**
   - Update `pyproject.toml` with your project name and description
   - Update `docker-compose.yaml` service names if needed
   - Update documentation and README files

### Customizing the Template

After cloning, you may want to customize:

- **Project name**: Update `app/pyproject.toml` and directory names
- **Database configuration**: Modify `app/app/settings.py` for your database setup
- **Environment variables**: Update `.env.example` with your specific configuration
- **Dependencies**: Add or remove packages in `app/pyproject.toml`
- **Documentation**: Update README files with your project-specific information

## 🏛️ Project Structure

```
layered-django-example/
├── docker-compose.yaml          # Multi-service Docker setup
├── Dockerfile                   # Application container definition
├── README.md                    # This file
└── app/                      # Django application
    ├── core/                    # Shared utilities and base classes
    ├── todo/                    # Todo application module
    │   ├── domain/              # Business logic and entities
    │   ├── application/         # Use cases and application services
    │   ├── data/                # Data access layer
    │   │   ├── models/          # Django ORM models
    │   │   └── elasticsearch/   # Search integration
    │   └── interfaces/          # External interfaces
    │       ├── views/           # API controllers
    │       ├── serializers/     # Data serialization
    │       └── schema/          # Pydantic schemas
    ├── manage.py                # Django management script
    ├── pyproject.toml           # Poetry dependencies
    └── README.md                # Application-specific documentation
```

## 🧩 Architecture Layers

### Domain Layer (`todo/domain/`)
- **Purpose**: Contains the core business logic and entities
- **Responsibilities**: 
  - Business rules and validation
  - Entity definitions
  - Domain services
- **Dependencies**: None (pure business logic)

### Application Layer (`todo/application/`)
- **Purpose**: Orchestrates use cases and application workflows
- **Responsibilities**:
  - Use case implementations
  - Application services
  - Workflow coordination
- **Dependencies**: Domain layer only

### Data Layer (`todo/data/`)
- **Purpose**: Handles data persistence and external data sources
- **Responsibilities**:
  - Database models (Django ORM)
  - Repository implementations
  - External service integrations (Elasticsearch)
- **Dependencies**: Domain layer

### Interface Layer (`todo/interfaces/`)
- **Purpose**: Handles external communication and data transformation
- **Responsibilities**:
  - API controllers (Django REST Framework views)
  - Data serialization
  - Input validation (Pydantic schemas)
- **Dependencies**: Domain and Application layers

## 🔧 Services

The application runs with the following services:

- **Django App**: Main web application (port 8000)
- **PostgreSQL**: Primary database (port 5432)
- **Redis**: Message broker for Celery (port 6379)
- **Celery Worker**: Background task processing

## 📖 API Documentation

The application provides RESTful API endpoints for managing todo lists and items. See the [app README](app/README.md) for detailed API documentation.

