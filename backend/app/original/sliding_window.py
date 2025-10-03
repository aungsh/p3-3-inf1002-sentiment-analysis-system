from collections import deque

#\backend\app\original\sliding_window.py
def afinn_sliding_window(scored_sentences, k=3):

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