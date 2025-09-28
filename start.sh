# Navigate and start backend
echo "Setting up backend..."
cd backend

# create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Run backend in background
uvicorn main:app --reload --port 8000 &

# Navigate to frontend
cd ../frontend
npm install
npm run dev
