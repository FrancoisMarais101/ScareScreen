# Build Stage
FROM python:3.12-bookworm as builder

# Install system packages required by your application.
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

# Copy application files
COPY . .

# Final Stage
FROM python:3.12-bookworm

# Install PostgreSQL client in the final stage
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies and application files from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /backend /backend

WORKDIR /backend

# Change permissions of the scripts before changing the user
COPY wait-for-db.sh /backend/wait-for-db.sh
COPY entrypoint.sh /backend/entrypoint.sh
RUN chmod +x /backend/wait-for-db.sh /backend/entrypoint.sh

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /backend
USER appuser

ENTRYPOINT ["/backend/entrypoint.sh"]
