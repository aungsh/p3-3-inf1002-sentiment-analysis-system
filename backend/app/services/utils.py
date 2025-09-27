from typing import List, Dict, Tuple
from app.services.sentiment import sentence_score, split_sentences, afinn_dict

# Sentence-level analysis
def per_sentence_analysis(text: str) -> List[Dict[str, int]]:
    sentences = split_sentences(text)
    return [{"sentence": s, "score": sentence_score(s, afinn_dict)} for s in sentences]

def analyze_text(text: str) -> Tuple[str, int]:
    results = per_sentence_analysis(text)
    total_score = sum(r["score"] for r in results)

    if total_score > 0:
        sentiment = "positive"
    elif total_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, total_score

def find_extremes(results: List[Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    if not results:
        return {"most_positive": None, "most_negative": None}
    return {
        "most_positive": max(results, key=lambda x: x["score"]),
        "most_negative": min(results, key=lambda x: x["score"]),
    }

# Sliding Window Analysis
def sliding_window(seq: List[str], window_size: int) -> List[List[str]]:
    return [seq[i:i+window_size] for i in range(len(seq) - window_size + 1)]

def analyze_sliding_windows(text: str, window_size: int = 3) -> Dict[str, Dict]:
    sentences = split_sentences(text)
    windows = sliding_window(sentences, window_size)

    scored_windows = []
    for window in windows:
        score = sum(sentence_score(s, afinn_dict) for s in window)
        scored_windows.append({"segment": " ".join(window), "score": score})

    if not scored_windows:
        return {"most_positive_segment": None, "most_negative_segment": None}

    return {
        "most_positive_segment": max(scored_windows, key=lambda x: x["score"]),
        "most_negative_segment": min(scored_windows, key=lambda x: x["score"]),
    }
