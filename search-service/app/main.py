from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.elasticsearch_client import index_document, search_documents

app = FastAPI()

@app.post("/index-document")
async def index_document_endpoint(document_id: str, metadata: dict):
    try:
        index_document(document_id, metadata)
        return JSONResponse(
            status_code=200,
            content={"message": "Document indexed successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search(query: str):
    try:
        results = search_documents(query)
        return JSONResponse(
            status_code=200,
            content={"message": "Search completed successfully", "results": results}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))