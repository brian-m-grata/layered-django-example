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

1. **Navigate to the sample directory**
   ```bash
   cd sample
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

## 🏛️ Project Structure

```
layered-django-example/
├── docker-compose.yaml          # Multi-service Docker setup
├── Dockerfile                   # Application container definition
├── README.md                    # This file
└── sample/                      # Django application
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

The application provides RESTful API endpoints for managing todo lists and items. See the [sample README](sample/README.md) for detailed API documentation.

