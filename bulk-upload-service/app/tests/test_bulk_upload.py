import pytest
from fastapi.testclient import TestClient
from app.main import app
from openpyxl import Workbook

client = TestClient(app)

def test_bulk_upload_csv():
    # Create a test CSV file
    with open("test_metadata.csv", "wb") as f:
        f.write(b"document_id,file_name,file_size\n1,example.pdf,1024\n2,sample.docx,2048")

    # Upload the CSV file
    with open("test_metadata.csv", "rb") as f:
        response = client.post("/bulk-upload", files={"file": f})

    # Assert the response
    assert response.status_code == 200
    assert response.json()["message"] == "Bulk upload completed successfully"

def test_bulk_upload_excel():
    # Create a test Excel file using openpyxl
    wb = Workbook()
    ws = wb.active
    ws.append(["document_id", "file_name", "file_size"])  # Header row
    ws.append([1, "example.pdf", 1024])  # First data row
    ws.append([2, "sample.docx", 2048])  # Second data row
    wb.save("test_metadata.xlsx")

    # Upload the Excel file
    with open("test_metadata.xlsx", "rb") as f:
        response = client.post("/bulk-upload", files={"file": f})

    # Assert the response
    assert response.status_code == 200
    assert response.json()["message"] == "Bulk upload completed successfully"