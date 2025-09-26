# backend/app/api/gemini.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.gemini import analyze_sentiment_gemini

router = APIRouter()

# Request model
class TextRequest(BaseModel):
    text: str

# POST /gemini_api/gemini
@router.post("/gemini")
def analyze_sentiment_gemini_api(request: TextRequest):
    results= analyze_sentiment_gemini(request.text)
    return results


