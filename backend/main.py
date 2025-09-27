# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# Create FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="API backend for sentiment analysis project",
    version="1.0.0",
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Health check endpoint
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Sentiment Analysis API running 🚀"}
