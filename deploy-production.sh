#!/bin/bash
# Production deployment script for VPS

set -e  # Exit on error

echo "🚀 LogSentry Production Deployment"
echo "===================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "❌ Please run as root (sudo)"
  exit 1
fi

# Configuration
APP_DIR="/opt/sentry"
DOMAIN="api.logsentry.io"
EMAIL="your@email.com"  # For Let's Encrypt

echo "📋 Deployment Configuration:"
echo "   App Directory: $APP_DIR"
echo "   Domain: $DOMAIN"
echo "   Email: $EMAIL"
echo ""

# Step 1: System updates
echo "📦 Step 1: Updating system..."
apt update && apt upgrade -y

# Step 2: Install Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Step 2: Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "✅ Step 2: Docker already installed"
fi

# Step 3: Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🐳 Step 3: Installing Docker Compose..."
    apt install docker-compose -y
else
    echo "✅ Step 3: Docker Compose already installed"
fi

# Step 4: Install Nginx
if ! command -v nginx &> /dev/null; then
    echo "🌐 Step 4: Installing Nginx..."
    apt install nginx -y
else
    echo "✅ Step 4: Nginx already installed"
fi

# Step 5: Install Certbot
if ! command -v certbot &> /dev/null; then
    echo "🔒 Step 5: Installing Certbot..."
    apt install certbot python3-certbot-nginx -y
else
    echo "✅ Step 5: Certbot already installed"
fi

# Step 6: Create app directory
echo "📁 Step 6: Creating app directory..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p /backups

# Step 7: Clone repository (if not exists)
if [ ! -d "$APP_DIR/.git" ]; then
    echo "📥 Step 7: Cloning repository..."
    echo "   Please enter your repository URL:"
    read REPO_URL
    git clone $REPO_URL $APP_DIR
else
    echo "✅ Step 7: Repository already cloned"
    cd $APP_DIR
    git pull origin main
fi

cd $APP_DIR

# Step 8: Setup environment file
echo "🔧 Step 8: Setting up environment..."
if [ ! -f ".env.production" ]; then
    echo "   Creating .env.production from example..."
    cp .env.production.example .env.production
    echo ""
    echo "⚠️  IMPORTANT: Edit .env.production with your credentials:"
    echo "   nano $APP_DIR/.env.production"
    echo ""
    read -p "Press Enter when done..."
else
    echo "✅ .env.production already exists"
fi

# Step 9: Setup Nginx configuration
echo "🌐 Step 9: Configuring Nginx..."

cat > /etc/nginx/sites-available/$DOMAIN << 'NGINX_CONFIG'
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=ingest_limit:10m rate=1000r/m;

upstream sentry_backend {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name api.logsentry.io;
    
    location / {
        proxy_pass http://sentry_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_CONFIG

# Enable site
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

# Reload nginx
systemctl reload nginx

echo "✅ Nginx configured"

# Step 10: Get SSL certificate
echo "🔒 Step 10: Getting SSL certificate..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL || echo "⚠️  SSL setup failed - you may need to configure DNS first"

# Step 11: Build and start containers
echo "🐳 Step 11: Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Step 12: Wait for health check
echo "⏳ Step 12: Waiting for backend to be healthy..."
sleep 10

if curl -f https://$DOMAIN/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend health check failed - check logs:"
    echo "   docker-compose -f docker-compose.prod.yml logs"
fi

# Step 13: Setup log rotation
echo "📝 Step 13: Setting up log rotation..."
cat > /etc/logrotate.d/sentry << 'LOGROTATE'
/opt/sentry/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        docker-compose -f /opt/sentry/docker-compose.prod.yml restart sentry-backend
    endscript
}
LOGROTATE

echo "✅ Log rotation configured"

# Step 14: Setup cron for auto-renewal
echo "🔄 Step 14: Setting up SSL auto-renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "Your backend is running at: https://$DOMAIN"
echo ""
echo "Next steps:"
echo "1. Deploy frontend to Vercel"
echo "2. Configure DNS for your frontend domain"
echo "3. Update Google OAuth with production URLs"
echo "4. Test the complete flow"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose -f docker-compose.prod.yml logs -f"
echo "  Restart:      docker-compose -f docker-compose.prod.yml restart"
echo "  Stop:         docker-compose -f docker-compose.prod.yml down"
echo "  Update code:  cd $APP_DIR && git pull && docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "Monitor health: curl https://$DOMAIN/health"
echo ""
