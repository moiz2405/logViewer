#!/bin/bash
# Activate the virtual environment
# Run the FastAPI app
source venv/bin/activate 

uvicorn main:app --reload
