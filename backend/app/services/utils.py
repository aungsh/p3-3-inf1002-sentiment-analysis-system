from app.services.sentiment import sentence_score, split_sentences, afinn_dict
from collections import deque

# (Jason) Sentence-level analysis
def per_sentence_analysis(text: str):
    # Split text into sentences
    sentences = split_sentences(text)
    
    # Analyze each sentence
    results = {}
    for idx, sentence in enumerate(sentences):
        if sentence:
            sentiment, score = analyze_text(sentence)
            results[idx] = {"text": sentence, "sentiment": sentiment, "score": score}
    return results

def analyze_text(text: str):
    score = sentence_score(text, afinn_dict)
    sentiment = "POSITIVE" if score > 0 else "NEGATIVE" if score < 0 else "NEUTRAL"
    return sentiment, score

def calculate_overall_score(text: str):

    if not text.strip():
        return {"overall_score": 0.0, "overall_sentiment": "NEUTRAL"}
    
    # Split into sentences
    sentences = split_sentences(text)
    
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

# (Aung) Module to find the most positive and most negative sentences based on their sentiment scores.
def find_extremes(sentence_scores):
    
    # Get the most positive and most negative sentences.
    if not sentence_scores:
        return None, None

    # Find the sentences with the highest and lowest scores
    most_positive = max(sentence_scores.values(), key=lambda x: x["score"])
    most_negative = min(sentence_scores.values(), key=lambda x: x["score"])

    return most_positive, most_negative

# (Saad) Sliding Window Analysis
def analyze_sliding_windows(scored_sentences, k):

    # Extract data from input dict
    sentences = [(data["text"], data["score"]) for key, data in scored_sentences.items() if key != "overall"]

    # Error handling for edge cases
    if len(sentences) < k:
        msg = f"[ERROR] Input must contain at least {k} sentences to form a sliding window."
        return ({"text": msg, "score": 0.0, "indices": None}, {"text": msg, "score": 0.0, "indices": None})

    # Fixed size sliding window of k sentences
    window = deque(maxlen=k)
    running_sum = 0

    # Dict for most positive/negative paragraphs, score, sentence indices
    best_positive = {'text': "", 'score': float('-inf'), "indices": None}
    best_negative = {'text': "", 'score': float('inf'), "indices": None}

    # Iterate through sentences with scores
    for i, (sentence, score) in enumerate(sentences):

        # Remove oldest score if window is full
        if len(window) == k:
            running_sum -= window[0][1]

        # Populate window with tuples of sentence + score
        window.append((sentence, score))
        running_sum += score

        # Save analyzed paragraph & avg score for window
        if len(window) == k:
            avg_score = running_sum / k
            joined_text = " ".join(s[0] for s in window)
            start_idx = i - k + 1
            end_idx = i

            # Assign paragraph & score to dictionary
            if avg_score > best_positive['score']:
                best_positive['score'] = round(avg_score, 2)
                best_positive['text'] = joined_text
                best_positive['indices'] = (start_idx, end_idx)

            if avg_score < best_negative['score']:
                best_negative['score'] = round(avg_score, 2)
                best_negative['text'] = joined_text
                best_negative['indices'] = (start_idx, end_idx)

    return best_positive, best_negative

# (Saad) Dynamic Window Analysis
def analyze_dynamic_windows(scored_sentences):
    # Extract data from scored reviews
    sentences = [(data["text"], data["score"]) for key, data in scored_sentences.items() if key != "overall"]
    n = len(sentences)

    # Edge case handling (Review length too short)
    if n < 2:
        msg = f"[ERROR] Need at least 2 sentences for dynamic analysis (found {n})."
        return (
            {"text": msg, "score": 0.0, "indices": None},
            {"text": msg, "score": 0.0, "indices": None},
        )

    # Initialize running sum and start indices
    pos_sum, neg_sum = 0, 0
    pos_start, neg_start = 0, 0

    # Initialize best segment dictionaries
    best_positive = {"text": "", "score": float('-inf'), "indices": None}
    best_negative = {"text": "", "score": float('inf'), "indices": None}

    for i, (text, score) in enumerate(sentences):
        # --- Positive segment logic ---
        if score <= 0:
            # Reset window if negative/neutral sentiment found
            pos_sum = 0
            pos_start = i + 1
        else:
            pos_sum += score
            if pos_sum > best_positive["score"]:
                best_positive["score"] = pos_sum
                best_positive["text"] = ". ".join(s[0] for s in sentences[pos_start:i+1])
                best_positive["indices"] = (pos_start, i)

        # --- Negative segment logic ---
        if score >= 0:
            # Reset window if positive/neutral sentiment found
            neg_sum = 0
            neg_start = i + 1
        else:
            neg_sum += score
            if neg_sum < best_negative["score"]:
                best_negative["score"] = neg_sum
                best_negative["text"] = ". ".join(s[0] for s in sentences[neg_start:i+1])
                best_negative["indices"] = (neg_start, i)

    # Handle cases with no positive/negative sentiment
    if best_positive["indices"] is None:
        best_positive["text"] = "[INFO] No positive sentiment found."
        best_positive["score"] = 0.0
        best_positive["indices"] = None
    if best_negative["indices"] is None:
        best_negative["text"] = "[INFO] No negative sentiment found."
        best_negative["score"] = 0.0
        best_negative["indices"] = None

    return best_positive, best_negative