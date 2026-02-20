# myApp Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY ./myApp/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy myApp code
COPY ./myApp /app

EXPOSE 8000
CMD ["bash", "start_server.sh"]
