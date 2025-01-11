import pandas as pd

def parse_metadata(file_path: str) -> list:
    try:
        # Read the file
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Only CSV and Excel files are allowed.")

        # Convert DataFrame to a list of dictionaries
        metadata_list = df.to_dict(orient="records")
        return metadata_list
    except Exception as e:
        raise Exception(f"Failed to parse metadata: {str(e)}")