# syntax=docker/dockerfile:1
FROM python:3.13-slim



# Upgrade pip (already included)
RUN pip install --upgrade pip

# Install curl (already included)



# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port
EXPOSE 5004

# Start the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5004"]