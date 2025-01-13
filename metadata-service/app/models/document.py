from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
import uuid
from ..config import (
    get_regions,
    get_countries,
    get_languages,
    get_categories,
    get_divisions,
    get_business_units,
    get_document_types
)

class DocumentMetadata(BaseModel):
    document_id: uuid.UUID
    document_title: str
    file_name: str
    file_size: int
    file_type: str
    upload_date: datetime
    last_modified_date: datetime
    user_id: uuid.UUID
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    storage_path: str
    version: int = 1
    checksum: str
    acl: Optional[Dict] = None
    thumbnail_path: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None
    division: Optional[str] = None
    business_unit: Optional[str] = None
    brand_id: Optional[uuid.UUID] = None
    document_type: str
    region: Optional[str] = Field(
        None,
        description="Region where document is applicable",
        example="EMEA"
    )
    country: Optional[str] = Field(
        None,
        description="Country where document is applicable",
        example="Germany"
    )
    languages: List[str] = Field(
        [],
        description="Languages supported by this document",
        example=["en", "de"]
    )
    alternate_part_numbers: List[str] = Field(
        [],
        description="Alternate part numbers for this document",
        example=["12345-A", "12345-B"],
        max_items=10
    )
    category: Optional[str] = Field(
        None,
        description="Document category",
        example="Technical Documentation"
    )
    division: Optional[str] = Field(
        None,
        description="Organizational division",
        example="Engineering"
    )
    business_unit: Optional[str] = Field(
        None,
        description="Business unit",
        example="Cloud Services"
    )
    document_type: str = Field(
        ...,
        description="Type of document",
        example="Manual"
    )

    @validator('region')
    def validate_region(cls, v):
        if v and v not in get_regions():
            raise ValueError(f"Invalid region. Must be one of: {', '.join(get_regions())}")
        return v

    @validator('country')
    def validate_country(cls, v, values):
        if v:
            if 'region' in values and values['region']:
                region_countries = get_countries().get(values['region'], [])
                if v not in region_countries:
                    raise ValueError(f"Invalid country for region {values['region']}")
            return v
        return None

    @validator('languages')
    def validate_languages(cls, v, values):
        if v and 'country' in values and values['country']:
            country_languages = get_languages().get(values['country'], [])
            invalid_languages = [lang for lang in v if lang not in country_languages]
            if invalid_languages:
                raise ValueError(f"Invalid languages for country {values['country']}: {', '.join(invalid_languages)}")
        return v

    @validator('category')
    def validate_category(cls, v):
        if v and v not in get_categories():
            raise ValueError(f"Invalid category. Must be one of: {', '.join(get_categories())}")
        return v

    @validator('division')
    def validate_division(cls, v):
        if v and v not in get_divisions():
            raise ValueError(f"Invalid division. Must be one of: {', '.join(get_divisions())}")
        return v

    @validator('business_unit')
    def validate_business_unit(cls, v):
        if v and v not in get_business_units():
            raise ValueError(f"Invalid business unit. Must be one of: {', '.join(get_business_units())}")
        return v

    @validator('document_type')
    def validate_document_type(cls, v):
        if v not in get_document_types():
            raise ValueError(f"Invalid document type. Must be one of: {', '.join(get_document_types())}")
        return v

class BrandMetadata(BaseModel):
    document_id: uuid.UUID
    available_countries: List[str]
    languages: List[str]
    brand_colors: List[str]
    brand_logo_path: str
    campaign_name: Optional[str] = None
    product_line: Optional[str] = None
