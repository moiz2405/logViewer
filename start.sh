#!/bin/bash
# Quick Start Script for Linux/Mac

echo "🚀 Starting Sentry Project..."
echo ""

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "❌ Error: .env.local not found!"
    echo "   Create .env.local from .env.example and fill in your Supabase credentials"
    exit 1
fi

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "   Please start Docker first"
    exit 1
fi

echo "✅ Environment check passed"
echo ""

# Start Docker services
echo "📦 Starting backend services (Docker)..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check if backend is responding
echo "🔍 Testing backend health..."
if curl -s http://localhost:8001/sdk/schema/validate > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend not responding yet (it may still be starting)"
fi

echo ""
echo "========================================"
echo "Services are starting!"
echo "========================================"
echo ""
echo "Backend (Sentry):  http://localhost:8001"
echo "Demo App (myApp):  http://localhost:8000"
echo ""
echo "Next steps:"
echo "1. Open a new terminal"
echo "2. cd frontend"
echo "3. npm install (first time only)"
echo "4. npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""
