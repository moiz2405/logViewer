# Quick Start Script for Windows
# This starts all services in the correct order

Write-Host "🚀 Starting Sentry Project..." -ForegroundColor Cyan
Write-Host ""

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    Write-Host "❌ Error: .env.local not found!" -ForegroundColor Red
    Write-Host "   Create .env.local from .env.example and fill in your Supabase credentials" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
}
catch {
    Write-Host "❌ Error: Docker is not running!" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop first" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Environment check passed" -ForegroundColor Green
Write-Host ""

# Start Docker services
Write-Host "📦 Starting backend services (Docker)..." -ForegroundColor Cyan
docker-compose up --build -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if backend is responding
Write-Host "🔍 Testing backend health..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/sdk/schema/validate" -Method Get -TimeoutSec 5
    if ($response.ok) {
        Write-Host "✅ Backend is healthy!" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠️  Backend not responding yet (it may still be starting)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend (Sentry):  http://localhost:8001" -ForegroundColor White
Write-Host "Demo App (myApp):  http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open a new terminal" -ForegroundColor White
Write-Host "2. cd frontend" -ForegroundColor White
Write-Host "3. npm install (first time only)" -ForegroundColor White
Write-Host "4. npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Then visit: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "To view logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "To stop: docker-compose down" -ForegroundColor Yellow
Write-Host ""
