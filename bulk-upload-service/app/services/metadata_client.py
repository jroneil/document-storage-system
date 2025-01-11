import httpx
from dotenv import load_dotenv
import os

load_dotenv()

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")

async def save_metadata(metadata: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{METADATA_SERVICE_URL}/save-metadata",
                json=metadata
            )
            if response.status_code != 200:
                raise Exception(f"Failed to save metadata: {response.text}")
    except Exception as e:
        raise Exception(f"Failed to send metadata to Metadata Service: {str(e)}")