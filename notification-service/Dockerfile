# syntax=docker/dockerfile:1
FROM python:3.13-slim



# Upgrade pip (already included)
RUN pip install --upgrade pip

# Install curl (already included)



# Copy requirements.txt and install dependencies
COPY requirements.txt .
# syntax=docker/dockerfile:1
# Use the latest stable Python 3.14 release, not the RC version
FROM python:3.14.0a3-bookworm



# Upgrade pip (already included)
RUN pip install --upgrade pip


# Copy requirements.txt and install dependencies
COPY requirements.txt .
#RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

#RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port
EXPOSE 5007

# Start the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5007"]