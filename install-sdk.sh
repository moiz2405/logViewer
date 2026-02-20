#!/bin/bash
# Helper script to install SDK in myApp container

echo "🔧 Installing Sentry SDK in myApp container..."
echo ""

# Check if container is running
if ! docker ps --filter "name=myapp-demo" --format "{{.Names}}" | grep -q myapp-demo; then
    echo "❌ Error: myapp-demo container is not running!"
    echo "   Start it first with: docker-compose up -d"
    exit 1
fi

echo "✅ Container is running"
echo ""

# Install SDK  
echo "📦 Installing SDK from local repository..."
if docker exec myapp-demo pip install -e /sdk/python > /dev/null 2>&1; then
    echo "✅ SDK installed successfully!"
else
    echo "❌ Failed to install SDK"
    exit 1
fi

echo ""
echo "========================================"
echo "Next steps:"
echo ""
echo "1. Go to http://localhost:3000/register"
echo "2. Create an app and copy the API key"
echo "3. Create docker-compose.override.yml:"
echo ""
cat << 'EOF'
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key-here
EOF
echo ""
echo "4. Run: docker-compose up -d myapp"
echo ""
echo "Or set the API key directly:"
echo "docker-compose exec myapp sh -c 'export SENTRY_API_KEY=your-key && python main.py'"
echo ""
