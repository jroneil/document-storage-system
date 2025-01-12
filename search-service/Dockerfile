FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python packages with retry
RUN pip install --no-cache-dir --retries 5 -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5005"]
