from fastapi import FastAPI

app = FastAPI(
    title="SentinelDocs API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SentinelDocs Backend Running"
    }

@app.get("/health", status_code=200)
def health():
    return {
        "status": "healthy"
    }