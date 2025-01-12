FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 5006

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5006"]
