import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def analyze_sentiment_gemini(text: str):
    """
    Analyze sentiment using Google Gemini.
    Returns: (sentiment, confidence)
    """
    client = genai.Client(api_key=api_key)

    try:
        # response = model.generate_content(prompt)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=f"Analyze the sentiment of this text: '{text}'. Return only the sentiment as POSITIVE, NEGATIVE, or NEUTRAL, and a confidence score between 0 and 1, separated by a comma. For example: POSITIVE,0.85"
        )

        result = response.text.strip()
        sentiment, confidence = result.split(',')
        sentiment = sentiment.strip().lower()
        confidence = float(confidence.strip())
        if sentiment not in ['positive', 'negative', 'neutral']:
            sentiment = 'neutral'
        if not (0 <= confidence <= 1):
            confidence = 0.5
    except Exception as e:
        sentiment = 'NEUTRAL'
        confidence = 0.5
    return sentiment, confidence