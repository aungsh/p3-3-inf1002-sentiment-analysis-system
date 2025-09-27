# Sentiment Analysis Using Python

In order to run the project, you need to have the following software installed on your machine:

- [Node.js](https://nodejs.org/en/download/) (for Next.js frontend)
- [Python](https://www.python.org/downloads/) (for FastAPI backend)
- [Git](https://git-scm.com/downloads) (for version control)

## Express Installation Instructions

1. Clone the repository

```
git clone https://github.com/aungsh/p3-3-inf1002-sentiment-analysis-system.git
cd p3-3-inf1002-sentiment-analysis-system
```

2. Run the setup script

On macOS/Linux:

```
bash start.sh
```

On Windows:

```
start.bat
```

This script will set up and run both the frontend and backend servers.

To close the servers, simply stop the terminal processes (Ctrl+C) twice.

## Manual Installation Instructions

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
├── frontend/                # Next.js frontend (React + TS + Tailwind + Shadcn)
│   ├── public/              # Static assets (logos, icons, etc.)
│   ├── src/
│   │   ├── app/             # Next.js app directory (routing, pages, layouts)
│   │   ├── components/      # Reusable UI components (buttons, cards, inputs)
│   │   ├── lib/             # Utility functions (formatting, API calls)
│   │   └── types/           # TypeScript type definitions
│   └── package.json
│
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── data/            # Static data files (e.g., afinn.txt)
│   │   ├── services/        # Utility modules and services
│   │   │   ├── gemini.py
│   │   │   ├── sentiment.py
│   │   │   └── utils.py
│   │   └── routes.py        # API routes
│   ├── main.py              # Entry point
│   ├── requirements.txt
│   ├── .env.example         # Example environment variables
│
├── .gitignore
├── start.sh                 # Script to setup and run both servers (macOS/Linux)
├── start.bat                # Script to setup and run both servers (Windows)
└── readme.md                # Project overview, setup instructions

```
