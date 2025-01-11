import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_bulk_upload_csv():
    with open("test_metadata.csv", "wb") as f:
        f.write(b"document_id,file_name,file_size\n1,example.pdf,1024\n2,sample.docx,2048")

    with open("test_metadata.csv", "rb") as f:
        response = client.post("/bulk-upload", files={"file": f})

    assert response.status_code == 200
    assert response.json()["message"] == "Bulk upload completed successfully"

def test_bulk_upload_excel():
    import pandas as pd
    df = pd.DataFrame({
        "document_id": [1, 2],
        "file_name": ["example.pdf", "sample.docx"],
        "file_size": [1024, 2048]
    })
    df.to_excel("test_metadata.xlsx", index=False)

    with open("test_metadata.xlsx", "rb") as f:
        response = client.post("/bulk-upload", files={"file": f})

    assert response.status_code == 200
    assert response.json()["message"] == "Bulk upload completed successfully"