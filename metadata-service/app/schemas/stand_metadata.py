from pydantic import BaseModel
from typing import Optional, Dict

class StandMetadataCreate(BaseModel):
    name: str
    location: str
    attributes: Optional[Dict] = None

class StandMetadataResponse(BaseModel):
    id: int
    name: str
    location: str
    attributes: Optional[Dict] = None