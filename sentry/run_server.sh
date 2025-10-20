#!/bin/bash
# Activate the virtual environment

# Run the FastAPI app on port 8001
uvicorn backend.app.main:app --reload --port 8001
