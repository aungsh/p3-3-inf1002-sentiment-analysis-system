# backend/app/core/sentiment_calculator.py
from afinn import Afinn

afinn = Afinn()

def analyze_text(text: str):
    """
    Analyze the sentiment of the input text using AFINN.
    Returns: (sentiment_label, score)
    """
    score = afinn.score(text)

    # Interpret score
    if score > 0:
        sentiment = "POSITIVE"
    elif score < 0:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return sentiment, score

def per_sentence_analysis(text: str):
    """
    Analyze sentiment per sentence.
    Returns an example hardcoded result.
    """     
    results = [
        ("I love programming.", "POSITIVE", 3),]
    
    return results