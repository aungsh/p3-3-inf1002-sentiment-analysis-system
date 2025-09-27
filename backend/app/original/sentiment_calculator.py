from afinn import Afinn
import re

afinn = Afinn()

def analyze_text(text: str):
    
    score = afinn.score(text)
    sentiment = "POSITIVE" if score > 0 else "NEGATIVE" if score < 0 else "NEUTRAL"
    return sentiment, score

def per_sentence_analysis(text: str):
   
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    # Analyze each sentence
    results = {}
    for idx, sentence in enumerate(sentences):
        if sentence:
            sentiment, score = analyze_text(sentence)
            results[idx] = {"text": sentence, "sentiment": sentiment, "score": score}
    return results

def calculate_overall_score(text: str):

    if not text.strip():
        return {"overall_score": 0.0, "overall_sentiment": "NEUTRAL"}
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    # Get scores per sentence
    scores = []
    for sentence in sentences:
        if sentence:
            _, score = analyze_text(sentence)
            scores.append(score)
    
    if not scores:  # no valid sentences
        return {"overall_score": 0.0, "overall_sentiment": "NEUTRAL"}
    
    # Average score per sentence
    overall_score = sum(scores) / len(scores)
    
    # Determine overall sentiment
    if overall_score > 0:
        sentiment = "POSITIVE"
    elif overall_score < 0:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    return {
        "overall_score": round(overall_score, 2),
        "overall_sentiment": sentiment
    }

