import os
import subprocess
import sys

# Function to create the project directory
def create_project_dir(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"Created project directory: {project_name}")
    else:
        print(f"Project directory '{project_name}' already exists.")

# Function to set up the virtual environment
def setup_virtualenv(project_name):
    venv_path = os.path.join(project_name, 'venv')
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print(f"Virtual environment created at: {venv_path}")
    else:
        print("Virtual environment already exists.")

# Function to create a requirements.txt file if it doesn't exist
def create_requirements_file(project_name):
    requirements_path = os.path.join(project_name, 'requirements.txt')
    if not os.path.exists(requirements_path):
        with open(requirements_path, 'w') as f:
            f.write("# Add your project dependencies here\n")
        print(f"Created an empty requirements.txt at: {requirements_path}")
    else:
        print("requirements.txt already exists.")

# Function to create a Dockerfile if it doesn't exist
def create_dockerfile(project_name):
    dockerfile_path = os.path.join(project_name, 'Dockerfile')
    if not os.path.exists(dockerfile_path):
        with open(dockerfile_path, 'w') as f:
            f.write(f"""# {project_name} Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
""")
        print(f"Created a Dockerfile at: {dockerfile_path}")
    else:
        print("Dockerfile already exists.")

# Function to create a README.md file if it doesn't exist
def create_readme_file(project_name):
    readme_path = os.path.join(project_name, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write(f"""# {project_name}

## Project Description
This is a Python project for {project_name}.

## Installation
1. Clone the repository.
2. Set up a virtual environment:
   ```bash
   python -m venv venv


