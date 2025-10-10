from fastapi import APIRouter
from pydantic import BaseModel
from app.services.utils import per_sentence_analysis, analyze_text, find_extremes, analyze_sliding_windows, analyze_dynamic_windows
from app.services.gemini import analyze_sentiment_gemini

router = APIRouter()

# Shared request model
class TextRequest(BaseModel):
    text: str

# Gemini API
@router.post("/gemini")
def analyze_sentiment_gemini_api(request: TextRequest):
    sentiment, confidence = analyze_sentiment_gemini(request.text)
    return {"sentiment": sentiment, "score": confidence}

# Sentiment API
@router.post("/sentiment/analyze")
def analyze_sentiment(request: TextRequest):
    sentiment, score = analyze_text(request.text)
    return {"sentiment": sentiment, "score": score}

@router.post("/sentiment/analyze_sentiment_per_sentence")
def analyze_sentiment_per_sentence(request: TextRequest):
    results = per_sentence_analysis(request.text)
    return results

# Extremes API
@router.post("/extremes")
def extremes(request: TextRequest):
    sentence_results = per_sentence_analysis(request.text) 
    extremes_results = find_extremes(sentence_results)      
    return extremes_results

class SlidingWindowRequest(BaseModel):
    text: str
    window_size: int = 3

# Sliding Window API
@router.post("/sliding_window")
def sliding_window(request: SlidingWindowRequest):
    sentence_results = per_sentence_analysis(request.text)
    window_results = analyze_sliding_windows(sentence_results, request.window_size)
    return window_results

# Dynamic Window API
@router.post("/dynamic_window")
def dynamic_window(request: TextRequest):
    sentence_results = per_sentence_analysis(request.text)
    window_results = analyze_dynamic_windows(sentence_results)
    return window_results

# API to call all functions and return a comprehensive analysis
@router.post("/full_analysis")
def full_analysis(request: SlidingWindowRequest):
    sentence_results = per_sentence_analysis(request.text)
    extremes_results = find_extremes(sentence_results)
    sliding_window_results = analyze_sliding_windows(sentence_results, request.window_size)
    overall_sentiment, overall_score = analyze_text(request.text)
    
    return {
        "overall": {
            "sentiment": overall_sentiment,
            "score": overall_score
        },
        "per_sentence": sentence_results,
        "extremes": extremes_results,
        "sliding_window": sliding_window_results,
    }
    
# @app.post("/wordcloud")
# def generate_wordcloud(data: dict = Body(...)):
#     text = data.get("text", "")
#     words = clean_text(text)

#     # Count top 30 words
#     freq = Counter(words).most_common(30)

#     # Convert to frontend format
#     word_list = [{"text": w, "value": c} for w, c in freq]

#     return word_list