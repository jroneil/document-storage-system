# syntax=docker/dockerfile:1
# Use the latest stable Python 3.14 release, not the RC version
FROM python:3.13.1-alpine3.21

RUN apk add --no-cache curl

# Upgrade pip (already included)
RUN pip install --upgrade pip

# Install curl (already included)


# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port
EXPOSE 5002

# Start the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5002"]
