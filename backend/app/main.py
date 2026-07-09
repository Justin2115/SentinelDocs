from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="SentinelDocs API",
    version="1.0.0",
    description="Backend API for SentinelDocs Document Management System"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to SentinelDocs API",
        "status": "running"
    }


@app.get("/health")
async def health():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "SentinelDocs Backend",
            "version": "1.0.0"
        }
    )