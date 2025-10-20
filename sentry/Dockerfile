# Sentry Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8001
CMD ["bash", "run_server.sh"]
