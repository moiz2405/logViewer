#!/bin/bash
# Activate the virtual environment
source venv/bin/activate

# Run the FastAPI app on port 8001
uvicorn backend.app.main:app --reload --port 8001
