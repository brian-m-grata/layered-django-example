FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    python3-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to not create virtual environment in container
RUN poetry config virtualenvs.create false

WORKDIR /app

# Copy Poetry configuration files from parent directory
COPY sample/pyproject.toml sample/poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY sample/ .

# Make startup script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

CMD ["./start.sh"]