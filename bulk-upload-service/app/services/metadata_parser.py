import csv
from openpyxl import load_workbook

def parse_metadata(file_path: str) -> list:
    try:
        metadata_list = []

        # Process CSV files
        if file_path.endswith(".csv"):
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    metadata_list.append(row)

        # Process Excel files
        elif file_path.endswith(".xlsx"):
            workbook = load_workbook(filename=file_path)
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1]]  # Read the header row

            for row in sheet.iter_rows(min_row=2, values_only=True):
                row_data = {headers[i]: row[i] for i in range(len(headers))}
                metadata_list.append(row_data)

        else:
            raise ValueError("Unsupported file type. Only CSV and Excel files are allowed.")

        return metadata_list

    except Exception as e:
        raise Exception(f"Failed to parse metadata: {str(e)}")