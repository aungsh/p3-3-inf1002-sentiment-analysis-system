from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from afinn import Afinn

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AFINN (simple sentiment lexicon)
afinn = Afinn()

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    score = afinn.score(request.text)

    # Interpret score
    if score > 0:
        sentiment = "POSITIVE"
    elif score < 0:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return {"sentiment": sentiment, "score": score}
