#!/bin/bash
# Activate the virtual environment

# Run the FastAPI app on port 8001
#!/bin/bash
source venv/bin/activate 

uvicorn backend.app.main:app --reload --port 8001
