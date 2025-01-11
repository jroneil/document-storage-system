from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.content_analysis import analyze_content

app = FastAPI()

@app.post("/analyze-content")
async def analyze_content_endpoint(text: str):
    try:
        result = analyze_content(text)
        return JSONResponse(
            status_code=200,
            content={"message": "Content analyzed successfully", "result": result}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))