# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=5009, reload=True)
