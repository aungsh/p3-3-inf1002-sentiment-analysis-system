from pathlib import Path
import re

STOPWORDS_PATH = Path(__file__).parent.parent / "data" / "stopwords.txt"
with open(STOPWORDS_PATH, encoding="utf-8") as f:
    STOPWORDS = set(line.strip().lower() for line in f if line.strip())
    
def clean_text(text: str):
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    return words