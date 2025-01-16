# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Tesseract OCR and pdf2image
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils  && rm -rf /var/lib/apt/lists/*
# Upgrade pip (already included)
RUN pip install --upgrade pip
# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5012", "run:app"]