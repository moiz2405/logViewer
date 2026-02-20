# Helper script to install SDK in myApp container
# Run this after getting your API key from the dashboard

Write-Host "🔧 Installing Sentry SDK in myApp container..." -ForegroundColor Cyan
Write-Host ""

# Check if container is running
$container = docker ps --filter "name=myapp-demo" --format "{{.Names}}"
if (-not $container) {
    Write-Host "❌ Error: myapp-demo container is not running!" -ForegroundColor Red
    Write-Host "   Start it first with: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Container is running" -ForegroundColor Green
Write-Host ""

# Install SDK
Write-Host "📦 Installing SDK from local repository..." -ForegroundColor Cyan
docker exec myapp-demo pip install -e /sdk/python 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ SDK installed successfully!" -ForegroundColor Green
}
else {
    Write-Host "❌ Failed to install SDK" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. Go to http://localhost:3000/register" -ForegroundColor White
Write-Host "2. Create an app and copy the API key" -ForegroundColor White
Write-Host "3. Create docker-compose.override.yml:" -ForegroundColor White
Write-Host ""
Write-Host @"
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key-here
"@ -ForegroundColor Gray
Write-Host ""
Write-Host "4. Run: docker-compose up -d myapp" -ForegroundColor White
Write-Host ""
Write-Host "Or set the API key directly:" -ForegroundColor Yellow
Write-Host "docker-compose exec myapp sh -c 'export SENTRY_API_KEY=your-key && python main.py'" -ForegroundColor Gray
Write-Host ""
