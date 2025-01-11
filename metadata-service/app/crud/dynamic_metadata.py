from app.models.mongo_models import metadata_collection

def create_dynamic_metadata(metadata: DynamicMetadataCreate):
    result = metadata_collection.insert_one(metadata.dict())
    return {"id": str(result.inserted_id)}

def get_dynamic_metadata(document_id: str):
    return metadata_collection.find_one({"document_id": document_id})