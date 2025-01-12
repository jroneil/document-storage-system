import json
from pathlib import Path
from typing import Dict, List

CONFIG_DIR = Path(__file__).parent.parent / "config"

def _load_config(filename: str) -> Dict:
    """Helper function to load JSON config files"""
    with open(CONFIG_DIR / filename) as f:
        return json.load(f)

def get_regions() -> List[str]:
    """Get list of available regions"""
    return _load_config("regions.json")["regions"]

def get_countries() -> Dict[str, List[str]]:
    """Get mapping of regions to countries"""
    return _load_config("countries.json")

def get_languages() -> Dict[str, List[str]]:
    """Get mapping of countries to languages"""
    return _load_config("countries.json")  # Reusing countries.json since it contains languages

def get_categories() -> List[str]:
    """Get list of document categories"""
    return _load_config("categories.json")["categories"]

def get_divisions() -> List[str]:
    """Get list of organizational divisions"""
    return _load_config("divisions.json")["divisions"]

def get_business_units() -> List[str]:
    """Get list of business units"""
    return _load_config("business_units.json")["business_units"]

def get_document_types() -> List[str]:
    """Get list of document types"""
    return _load_config("document_types.json")["document_types"]
