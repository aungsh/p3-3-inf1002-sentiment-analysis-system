# backend/app/core/sentiment_calculator.py
import nltk
import re
from afinn import Afinn

nltk.download('punkt') 
afinn = Afinn()

def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^\w\s.!?]', '', text)
    return text.lower().strip()

def analyze_text(text: str):
    """
    Analyze the sentiment of the input text using AFINN.
    Returns: (sentiment_label, score)
    """
    cleaned_text = preprocess_text(text)
    if not cleaned_text:
        return "NEUTRAL", 0
    
    raw_score = afinn.score(cleaned_text)
    normalized_score = max(min(10 * raw_score / 50, 10), -10)

    # Interpret score
    if normalized_score > 5:
        sentiment = "VERY_POSITIVE"
    elif normalized_score > 0:
        sentiment = "POSITIVE"
    elif normalized_score < -5:
        sentiment = "VERY_NEGATIVE"
    elif normalized_score < 0:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return sentiment, normalized_score

def per_sentence_analysis(text: str):
    """
    Analyze sentiment per sentence.
    Returns an example hardcoded result.
    """     
    cleaned_text = preprocess_text(text)
    if not cleaned_text:
        return {0: {"text": "No valid text", "score": 0, "sentiment": "NEUTRAL"}}
    
    sentences = nltk.sent_tokenize(cleaned_text)
    sentences_scores = {}
    raw_scores = []
    
    for idx, sentence in enumerate(sentences):
        raw_score = afinn.score(sentence)
        normalized_score = max(min(10 * raw_score / 20, 10), -10)

        if normalized_score > 5:
            sentiment = "VERY_POSITIVE"
        elif normalized_score > 0:
            sentiment = "POSITIVE"
        elif normalized_score < -5:
            sentiment = "VERY_NEGATIVE"
        elif normalized_score < 0:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"

        sentences_scores[idx] = {"text": sentence, "score": normalized_score, "sentiment": sentiment}
        raw_scores.append(raw_score)

    if raw_scores:
        overall_raw_score = sum(raw_scores)
    else:
        overall_raw_score = 0

    overall_score = max(min(10 * overall_raw_score / 50, 10), -10)

    if overall_score > 5:
        overall_sentiment = "VERY_POSITIVE"
    elif overall_score > 0:
        overall_sentiment = "POSITIVE"
    elif overall_score < -5:
        overall_sentiment = "VERY_NEGATIVE"
    elif overall_score < 0:
        overall_sentiment = "NEGATIVE"
    else:
        overall_sentiment = "NEUTRAL"
    
    sentences_scores["overall"] = {"sentiment": overall_sentiment, "score": overall_score}
    
    return sentences_scores
