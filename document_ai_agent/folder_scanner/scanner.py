# scanner.py
import os
import time
import requests

# Configuration
SCAN_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scan_folder')  # Folder to monitor
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../uploads')  # Folder to move processed files
API_URL = 'http://localhost:5000/upload'  # URL of the Document AI Agent

def upload_file(file_path):
    """
    Uploads a file to the Document AI Agent via the /upload endpoint.
    """
    with open(file_path, 'rb') as file:
        response = requests.post(API_URL, files={'file': file})
        if response.status_code == 200:
            print(f"Uploaded {file_path}: {response.json()}")
        else:
            print(f"Failed to upload {file_path}: {response.text}")

def scan_folder():
    """
    Scans the folder for new files and uploads them to the Document AI Agent.
    """
    for filename in os.listdir(SCAN_FOLDER):
        file_path = os.path.join(SCAN_FOLDER, filename)
        if os.path.isfile(file_path):
            try:
                upload_file(file_path)
                # Move the file to the uploads folder after processing
                os.rename(file_path, os.path.join(UPLOAD_FOLDER, filename))
                print(f"Moved {filename} to uploads folder")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == '__main__':
    while True:
        scan_folder()
        time.sleep(300)  # Scan every 5 minutes