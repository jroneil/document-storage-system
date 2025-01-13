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
        
#Function to create a Dockerfile file if it doesn't exist
def create_dockerfile_file(project_name):
    dockerfile_path = os.path.join(project_name, 'Dockerfile')
    if not os.path.exists(dockerfile_path):
        with open(dockerfile_path, 'w') as f:
            f.write("# "+project_name)
        print(f"Created an empty Dockerfile at: {dockerfile_path}")
    else:
        print("DockerRile already exists.")
#Function to create a Dockerfile file if it doesn't exist

# Function to install dependencies from requirements.txt
def install_dependencies(project_name):
    requirements_path = os.path.join(project_name, 'requirements.txt')
    if os.path.exists(requirements_path):
        subprocess.check_call([
            os.path.join(project_name, 'venv', 'bin', 'pip') if os.name != 'nt' else os.path.join(project_name, 'venv', 'Scripts', 'pip'),
            'install', '-r', requirements_path
        ])
        print("Dependencies installed from requirements.txt.")
    else:
        print("No requirements.txt file found. Skipping dependency installation.")

# Function to update requirements.txt with current environment packages
def update_requirements_file(project_name):
    venv_pip = os.path.join(project_name, 'venv', 'bin', 'pip') if os.name != 'nt' else os.path.join(project_name, 'venv', 'Scripts', 'pip')
    requirements_path = os.path.join(project_name, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        subprocess.check_call([venv_pip, 'freeze'], stdout=f)
    print("requirements.txt has been updated with current dependencies.")

# Main function to execute the setup
def main():
    project_name = input("Enter the project name: ").strip()
    if not project_name:
        print("Project name cannot be empty.")
        return

    print("Choose an option:")
    print("1. Create a new project")
    print("2. Update requirements.txt")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        create_project_dir(project_name)
        setup_virtualenv(project_name)
        create_requirements_file(project_name)
        create_dockerfile_file(project_name);
        install_dependencies(project_name)
        update_requirements_file(project_name)
    elif choice == "2":
        update_requirements_file(project_name)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()


