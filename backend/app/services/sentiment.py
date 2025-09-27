import re
from pathlib import Path
from typing import List, Dict

# Load AFINN lexicon
def load_afinn(filepath: str) -> Dict[str, int]:
    afinn = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word, score = line.strip().split("\t")
            afinn[word] = int(score)
    return afinn

# Text Processing
def tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())

def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"[.!?]+", text)
    return [s.strip() for s in sentences if s.strip()]

# Sentiment Scoring
def sentence_score(sentence: str, afinn: Dict[str, int]) -> int:
    tokens = tokenize(sentence)
    return sum(afinn.get(token, 0) for token in tokens)

# Initialize dictionary (loaded once)
AFINN_PATH = Path(__file__).parent.parent / "data" / "afinn.txt"
afinn_dict = load_afinn(str(AFINN_PATH))
