#!/bin/bash
# Activate the virtual environment

# Run the FastAPI app on port 8001
#!/bin/bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8001
