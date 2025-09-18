# Sentiment Analysis Using Python

## Installation Instructions

In order to run the project, you need to have the following software installed on your machine:

- [Node.js](https://nodejs.org/en/download/) (for Next.js frontend)
- [Python](https://www.python.org/downloads/) (for FastAPI backend)
- [Git](https://git-scm.com/downloads) (for version control)

Both the frontend and backend servers need to be running simultaneously for the application to function correctly.

### Initialise Frontend NextJS server

1. Change directory to frontend folder

```
cd frontend
```

2. Install node packages (only required for first instllation or updates to package.json)

```
npm install
```

3. Run development server

```
npm run dev
```

The default port is 3000.
To view the web page, open `http://localhost:3000` in the browser.

### Initialise Backend FastAPI server

1. Change directory to backend folder

```
cd backend
```

2. Create virtual environment (only required for first instllation)

```
python3 -m venv venv
```

3. Activate virtual environment

On Windows:

```
venv\Scripts\activate
```

On macOS/Linux:

```
source venv/bin/activate
```

4. Install python packages (only required for first instllation or updates to requirements.txt)

```
pip install -r requirements.txt
```

5. Run FastAPI server

```
uvicorn main:app --reload --port 8000
```

## Folder Structure

```
monorepo-sentiment-analysis/
│
├── frontend/                           # Next.js frontend (React + TS + Tailwind + Shadcn)
│   ├── public/                         # Static assets (logos, icons, etc.)
│   ├── src/
│   │   ├── app/                        # Next.js app directory (routing, pages, layouts)
│   │   ├── components/                 # Reusable UI components (buttons, cards, inputs)
│   │   ├── lib/                        # Utility functions (formatting, API calls)
│   │   └── types/                      # TypeScript type definitions
│   └── package.json
│
├── backend/                            # FastAPI backend (Python)
│   ├── app/
│   │   ├── api/                        # REST API routes
│   │   │   ├── sentiment.py            # Endpoints for sentiment scoring
│   │   │   └── gemini.py               # Endpoint to call Gemini API
│   │   ├── core/                       # Core sentiment analysis logic
│   │   │   ├── afinn_loader.py         # Load and use AFINN lexicon
│   │   │   ├── sentiment_calculator.py # Sentence scoring, avg score, sliding window
│   │   │   └── extremes.py             # Identify most positive/negative sentences
│   │   ├── models/                     # Pydantic models for request/response validation
│   │   ├── services/                   # Integration services (Gemini API, etc.)
│   │   ├── utils/                      # Helper functions (text preprocessing, tokenization)
│   │   └── main.py                     # FastAPI entry point (with Uvicorn)
│   └── requirements.txt
│
├── .gitignore
└── README.md                           # Project overview, setup instructions
```
