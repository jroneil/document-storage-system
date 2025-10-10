# syntax=docker/dockerfile:1
FROM python:3.13.1-alpine3.21

# Install system dependencies for Alpine
RUN apk add --no-cache \
    curl \
    gcc \
    g++ \
    libffi-dev \
    openssl-dev \
    python3-dev \
    musl-dev \
    build-base

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5005"]
