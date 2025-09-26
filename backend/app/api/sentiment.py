# backend/app/api/sentiment.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.sentiment_calculator import analyze_text
from app.core.sentiment_calculator import per_sentence_analysis

router = APIRouter()

# Request model
class TextRequest(BaseModel):
    text: str

# POST /sentiment/analyze
@router.post("/analyze")
def analyze_sentiment(request: TextRequest):
    sentiment, score = analyze_text(request.text)
    return {"sentiment": sentiment, "score": score}

@router.post("/analyze_sentiment_per_sentence")
def analyze_sentiment_per_sentence(request: TextRequest):
    results = per_sentence_analysis(request.text)
    #return {"results": [{"sentence": s, "sentiment": sentiment, "score": score} for s, sentiment, score in results]}
    return {"results": results}
    #return {[{"sentence": s, "sentiment": sentiment, "score": score} for s, sentiment, score in results]}