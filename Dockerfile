# Stage 1: Build dependencies with Poetry
FROM python:3.10-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock /app/

# Install dependencies in a temporary directory
RUN poetry export --without-hashes -o requirements.txt

# Stage 2: Final lightweight runtime image
FROM python:3.10-slim

# Create a User and Group for the application
RUN useradd --create-home --home-dir /app --shell /bin/bash python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy pre-built requirements from builder
COPY --from=builder /app/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY core /app/core
COPY api_v1 /app/api_v1
COPY optimization /app/optimization
COPY stats /app/stats
COPY multitaskill /app/multitaskill
COPY multitaskill /app/multitaskill
COPY manage.py /app/manage.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Change ownership of the application code
RUN chown -R python:python /app
RUN chmod -R 700 /app

USER python

# Expose the Django port
EXPOSE 8000

# Use gunicorn for production
CMD ["gunicorn", "multitaskill.wsgi", "--bind", "0.0.0.0:8000", "--workers", "3"]