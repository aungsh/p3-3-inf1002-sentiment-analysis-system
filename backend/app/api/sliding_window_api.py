
from fastapi import APIRouter
from pydantic import BaseModel
import httpx
from app.core.sliding_window import afinn_sliding_window

router = APIRouter()

# Request model
class TextRequest(BaseModel):
    text: str

# POST /sliding_window_api/sliding_window
@router.post("/sliding_window")
def sliding_window(request: TextRequest):
    #call the function from analyze_sentiment_per_sentence
    response=httpx.post("http://localhost:8000/sentiment/analyze_sentiment_per_sentence", json={"text": request.text})
    #print('this is my response:')
    #print(response.json())
    results = afinn_sliding_window(response.json())
    #return {"results": [{"sentence": s, "sentiment": sentiment, "score": score} for s, sentiment, score in results]}
    return results