# Use a Debian-based Python image
FROM python:3.13-slim

# Upgrade pip
RUN pip install --upgrade pip

# Install necessary build tools for other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libffi-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set an environment variable to ensure prebuilt binaries are used
ENV TORCH_CUDA_ARCH_LIST="all"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the app port
EXPOSE 5006

# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5006"]
