import time
from folder_scanner.scanner import scan_folder

if __name__ == '__main__':
    while True:
        scan_folder()
        time.sleep(300)  # Scan every 5 minutes