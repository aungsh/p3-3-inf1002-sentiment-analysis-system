# backend/app/api/sentiment.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.sliding_window import afinn_sliding_window

router = APIRouter()

# Request model
class TextRequest(BaseModel):
    text: str

# POST /sliding_window_api/sliding_window
@router.post("/sliding_window")
def afinn_sliding_windows(request: TextRequest):
    #call the function from analyze_sentiment_per_sentence
    

    results = afinn_sliding_window(request.text)
    #return {"results": [{"sentence": s, "sentiment": sentiment, "score": score} for s, sentiment, score in results]}
    return results