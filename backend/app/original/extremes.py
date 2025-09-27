# Module to find the most positive and most negative sentences based on their sentiment scores.

def get_extremes(sentence_scores):
    
    # Get the most positive and most negative sentences.
    if not sentence_scores:
        return None, None

    # Find the sentences with the highest and lowest scores
    most_positive = max(sentence_scores.values(), key=lambda x: x["score"])
    most_negative = min(sentence_scores.values(), key=lambda x: x["score"])

    return most_positive, most_negative

# Call the function and print the results
if __name__ == "__main__":
    
    # Sample data structure for sentence scores
    sentence_scores = {
        0: {"text": "I love this product!", "score": 0.8},
        1: {"text": "It's okay I guess.", "score": 0.1},
        2: {"text": "Terrible experience.", "score": -0.7}
    }
    
    pos, neg = get_extremes(sentence_scores)
    print("Most positive:", pos)
    print("Most negative:", neg)
