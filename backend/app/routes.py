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

# example output
# {
#     "sentiment": "neutral", # POSITIVE, NEGATIVE, NEUTRAL
#     "score": 0.7
# }

# Sentiment API
@router.post("/sentiment/analyze")
def analyze_sentiment(request: TextRequest):
    sentiment, score = analyze_text(request.text)
    return {"sentiment": sentiment, "score": score}

# example output
# {
#     "sentiment": "negative",
#     "score": -3
# }

@router.post("/sentiment/analyze_sentiment_per_sentence")
def analyze_sentiment_per_sentence(request: TextRequest):
    results = per_sentence_analysis(request.text)
    return results

# example output
# [
#     {
#         "sentence": "I am sad",
#         "score": -2
#     },
#     {
#         "sentence": "I am neutral",
#         "score": 0
#     },
#     {
#         "sentence": "I am chilling",
#         "score": -1
#     }
# ]

# Extremes API
@router.post("/extremes")
def extremes(request: TextRequest):
    sentence_results = per_sentence_analysis(request.text) 
    extremes_results = find_extremes(sentence_results)      
    return extremes_results

# example output
# {
#     "most_positive": {
#         "sentence": "I am neutral",
#         "score": 0
#     },
#     "most_negative": {
#         "sentence": "I am sad",
#         "score": -2
#     }
# }

# Sliding Window API
@router.post("/sliding_window")
def sliding_window(request: TextRequest):
    sentence_results = per_sentence_analysis(request.text)
    window_results = analyze_sliding_windows(sentence_results)
    return window_results

# example output
# {
#     "best_positive": {
#         "text": "I am good. very cool. nice",
#         "score": 1.00,
#         "indices": (3, 5) 
#     },
#     "best_negative": {
#         "text": "I am sad. this sucks. so bad",
#         "score": -2.00,
#         "indices": (0, 2)
#     }
# }

# Dynamic Window API
@router.post("/dynamic_window")
def dynamic_window(request: TextRequest):
    sentence_results = per_sentence_analysis(request.text)
    window_results = analyze_dynamic_windows(sentence_results)
    return window_results

# example output
# {
#     "best_positive": {
#         "text": "This is good. very cool",
#         "score": 1.00,
#         "indices": (4, 5) 
#     },
#     "best_negative": {
#         "text": "I am sad. this sucks. so bad. very boring",
#         "score": -2.00,
#         "indices": (0, 3)
#     }
# }