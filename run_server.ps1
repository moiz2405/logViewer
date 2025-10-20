# Activate the virtual environment
winenv\Scripts\Activate.ps1

# Run the FastAPI app on port 8001
uvicorn backend.app.main:app --reload --port 8001
