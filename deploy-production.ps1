# Production Deployment Script for VPS (Windows Development)
# Run this on your VPS via SSH

$ErrorActionPreference = "Stop"

Write-Host "🚀 LogSentry Production Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script should be run on your VPS (Ubuntu/Debian)" -ForegroundColor Yellow
Write-Host ""

Write-Host "Steps to deploy:" -ForegroundColor Green
Write-Host ""
Write-Host "1. SSH into your VPS:" -ForegroundColor White
Write-Host "   ssh root@your-vps-ip" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Download and run the deployment script:" -ForegroundColor White
Write-Host "   curl -fsSL https://raw.githubusercontent.com/yourname/sentry/main/deploy-production.sh -o deploy.sh" -ForegroundColor Gray
Write-Host "   chmod +x deploy.sh" -ForegroundColor Gray
Write-Host "   sudo ./deploy.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "Or manually:" -ForegroundColor White
Write-Host "   1. Copy deploy-production.sh to your VPS" -ForegroundColor Gray
Write-Host "   2. Run: chmod +x deploy-production.sh" -ForegroundColor Gray
Write-Host "   3. Run: sudo ./deploy-production.sh" -ForegroundColor Gray
Write-Host ""

# Generate deployment checklist
Write-Host "📋 Pre-Deployment Checklist:" -ForegroundColor Cyan
Write-Host "   [ ] VPS provisioned (DigitalOcean, Hetzner, AWS, etc.)" -ForegroundColor White
Write-Host "   [ ] Domain purchased (api.logsentry.io)" -ForegroundColor White
Write-Host "   [ ] DNS A record points to VPS IP" -ForegroundColor White
Write-Host "   [ ] Supabase project created" -ForegroundColor White
Write-Host "   [ ] Database migrations ready" -ForegroundColor White
Write-Host "   [ ] Google OAuth credentials created" -ForegroundColor White
Write-Host "   [ ] GitHub repository pushed" -ForegroundColor White
Write-Host ""

Write-Host "✅ Ready to deploy? Follow the steps above!" -ForegroundColor Green
