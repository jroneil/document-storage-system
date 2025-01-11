# app/utils/validators.py
from pydantic import BaseModel, validator
from typing import Dict

def validate_metadata(metadata: Dict, required_fields: Dict):
    for field, field_type in required_fields.items():
        if field not in metadata:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(metadata[field], field_type):
            raise ValueError(f"Field {field} must be of type {field_type}")
    return metadata