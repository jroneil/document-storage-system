from pymongo import MongoClient
from app.models.document import BrandMetadata
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["metadata_db"]
metadata_collection = db["dynamic_metadata"]

def save_brand_metadata(brand_metadata: BrandMetadata):
    try:
        result = metadata_collection.insert_one(brand_metadata.dict())
        return result.inserted_id
    except Exception as e:
        raise Exception(f"Failed to save brand metadata: {str(e)}")

def delete_brand_metadata(document_id: str):
    try:
        metadata_collection.delete_one({"document_id": document_id})
        return True
    except Exception as e:
        raise Exception(f"Failed to delete brand metadata: {str(e)}")