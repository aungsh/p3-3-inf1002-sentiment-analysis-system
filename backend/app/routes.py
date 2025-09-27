from fastapi import APIRouter
from pydantic import BaseModel
import httpx

# Import your core logic
from app.core.gemini import analyze_sentiment_gemini
from app.core.sentiment_calculator import analyze_text, per_sentence_analysis
from app.core.sliding_window import afinn_sliding_window

router = APIRouter()

# Shared request model
class TextRequest(BaseModel):
    text: str

# =========================
# Gemini API
# =========================
@router.post("/gemini")
def analyze_sentiment_gemini_api(request: TextRequest):
    results = analyze_sentiment_gemini(request.text)
    return results

# =========================
# Sentiment API
# =========================
@router.post("/sentiment/analyze")
def analyze_sentiment(request: TextRequest):
    sentiment, score = analyze_text(request.text)
    return {"sentiment": sentiment, "score": score}

@router.post("/sentiment/analyze_sentiment_per_sentence")
def analyze_sentiment_per_sentence(request: TextRequest):
    results = per_sentence_analysis(request.text)
    return {"results": results}

# =========================
# Sliding Window API
# =========================
@router.post("/sliding_window")
def sliding_window(request: TextRequest):
    # Call existing sentiment per-sentence API locally
    response = httpx.post(
        "http://localhost:8000/sentiment/analyze_sentiment_per_sentence",
        json={"text": request.text}
    )
    results = afinn_sliding_window(response.json()["results"])
    return results
