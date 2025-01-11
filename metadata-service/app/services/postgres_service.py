import psycopg2
from app.models.document import DocumentMetadata
from dotenv import load_dotenv
import os

load_dotenv()

def save_document_metadata(document_metadata: dict):
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = connection.cursor()

        query = """
        INSERT INTO documents (
            document_id, file_name, file_size, file_type, upload_date, last_modified_date,
            user_id, tags, description, storage_path, version, checksum, acl, thumbnail_path,
            expiration_date, category, division, business_unit, brand_id, document_type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            document_metadata["document_id"], document_metadata["file_name"], document_metadata["file_size"],
            document_metadata["file_type"], document_metadata["upload_date"], document_metadata["last_modified_date"],
            document_metadata["user_id"], document_metadata["tags"], document_metadata["description"],
            document_metadata["storage_path"], document_metadata["version"], document_metadata["checksum"],
            document_metadata["acl"], document_metadata["thumbnail_path"], document_metadata["expiration_date"],
            document_metadata["category"], document_metadata["division"], document_metadata["business_unit"],
            document_metadata["brand_id"], document_metadata["document_type"]
        ))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        raise Exception(f"Failed to save document metadata: {str(e)}")

def delete_document_metadata(document_id: str):
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = connection.cursor()

        query = "DELETE FROM documents WHERE document_id = %s"
        cursor.execute(query, (document_id,))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        raise Exception(f"Failed to delete document metadata: {str(e)}")