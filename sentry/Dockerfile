# Sentry Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY ./sentry/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY ./sentry /app

EXPOSE 8001
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
