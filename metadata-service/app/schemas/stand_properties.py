from pydantic import BaseModel
from typing import Optional, Dict

class StandPropertiesCreate(BaseModel):
    name: str
    location: str
    attributes: Optional[Dict] = None

class StandPropertiesResponse(BaseModel):
    id: int
    name: str
    location: str
    attributes: Optional[Dict] = None