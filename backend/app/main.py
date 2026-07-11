from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="DocSentinel API",
    version="1.0.0",
    description="Backend API for the DocSentinel Document Management System"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocSentinel API",
        "status": "running"
    }

@app.get("/health")
async def health():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "DocSentinel Backend",
            "version": "1.0.0"
        }
    )