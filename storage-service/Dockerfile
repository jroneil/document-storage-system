# syntax=docker/dockerfile:1
FROM python:3.11-slim


# Upgrade pip (already included)
RUN pip install --upgrade pip

WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5003"]