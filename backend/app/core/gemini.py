from google import genai

def analyze_sentiment_gemini(text: str):
    """
    Analyze sentiment using Google Gemini.
    Returns: (sentiment, confidence)
    """
    client = genai.Client()

    try:
        # response = model.generate_content(prompt)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=f"Analyze the sentiment of this text: '{text}'. Return only the sentiment as POSITIVE, NEGATIVE, or NEUTRAL, and a confidence score between 0 and 1, separated by a comma. For example: POSITIVE,0.85"
        )
    # print(response.text)
        result = response.text.strip()
        sentiment, confidence = result.split(',')
        sentiment = sentiment.strip().upper()
        confidence = float(confidence.strip())
        if sentiment not in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
            sentiment = 'NEUTRAL'
        if not (0 <= confidence <= 1):
            confidence = 0.5
    except Exception as e:
        sentiment = 'NEUTRAL'
        confidence = 0.5
    return sentiment, confidence


if __name__ == "__main__":

    text = "I love cherry"
    sentiment, confidence = analyze_sentiment_gemini(text)
    print(sentiment, confidence)

    
# # POST /gemini/analyze
# @router.post("/analyze")
# def analyze_sentiment_gemini_endpoint(request: TextRequest):
#     sentiment, confidence = analyze_sentiment_gemini(request.text)
#     return {"sentiment(gemini)": sentiment, "confident(gemini)": confidence}

# # POST /gemini/analyze_per_sentence
# @router.post("/analyze_per_sentence")
# def analyze_sentiment_per_sentence_gemini(request: TextRequest):
#     # Simple sentence splitting
#     sentences = request.text.split('.')
#     results = []
#     for sentence in sentences:
#         if sentence.strip():
#             sentiment, confidence = analyze_sentiment_gemini(sentence.strip())
#             results.append({"sentence": sentence.strip(), "sentiment(gemini)": sentiment, "confident(gemini)": confidence})
#     return {"results": results}