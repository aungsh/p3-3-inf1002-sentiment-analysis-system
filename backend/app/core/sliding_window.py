from collections import deque

# p3-3-inf1002-sentiment-analysis-system\backend\app\core\sliding_window.py
def afinn_sliding_window(scored_sentences):

    # Fixed size sliding window of 3 sentences
    window = deque(maxlen=3)
    running_sum = 0

    # Dict for most positive/negative paragaphs + score
    best_positive = {'score': float('-inf'), 'text': ""}
    best_negative = {'score': float('inf'), 'text': ""}

    for sentence, score in scored_sentences.items():

        # Remove oldest score if window is full
        if len(window) == 3:
            running_sum -= window[0][1]

        # Populate window with tuples of sentence + score
        window.append((sentence, score))
        running_sum += score

        # Save analyzed paragraph & avg score for window
        if len(window) == 3:
            avg_score = running_sum / 3
            joined_text = " ".join(s[0] for s in window)

            # assign paragraph & score to dictionary
            if avg_score > best_positive['score']:
                best_positive['score'] = avg_score
                best_positive['text'] = joined_text

            if avg_score < best_negative['score']:
                best_negative['score'] = avg_score
                best_negative['text'] = joined_text

    # Tuples of (text, score). return most_positive, most_negative if want as dictionary
    return (best_positive['text'], best_positive['score']), (best_negative['text'], best_negative['score'])