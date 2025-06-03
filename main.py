import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from src.api.routes import router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Trend Monitor",
    description="Monitor and implement trending AI technologies",
    version="1.0.0"
)

# Include the router
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Trend Monitor",
        "status": "active"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 