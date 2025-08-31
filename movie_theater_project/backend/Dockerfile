# Use a lightweight Python base image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build dependencies
FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM base AS final

# Copy installed dependencies
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# Add a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

# Expose the application port
EXPOSE 8000

# Add a health check
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run the application
CMD ["gunicorn", "movie_theater.wsgi:application", "--bind", "0.0.0.0:8000"]