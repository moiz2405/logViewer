# LogViewer FastAPI Backend

A high-performance, real-time log processing and monitoring system built with FastAPI. This backend receives log streams from multiple microservices, processes them continuously using AI classification, and provides real-time health monitoring through WebSocket connections.

## 🚀 Features

- **Real-time Log Streaming**: Continuous log ingestion from multiple microservices
- **AI-Powered Classification**: Intelligent log analysis using Agno + Groq integration  
- **Health Monitoring**: Real-time service health tracking and alerting
- **WebSocket Support**: Live updates for dashboards and monitoring tools
- **Analytics Engine**: Advanced log analytics with pattern detection
- **Notification System**: Multi-channel alerts (email, Slack, webhooks)
- **Scalable Architecture**: Designed for high-throughput log processing

## 📁 Project Structure

```
backend/
├── main.py                     # FastAPI application entry point
├── run_server.py              # Server startup script
├── test_backend.py            # Backend structure test
├── install_deps.py            # Dependency installer
├── app/
│   ├── __init__.py
│   ├── api/                   # API route definitions
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── logs.py        # Log streaming endpoints
│   │       ├── health.py      # Health monitoring endpoints  
│   │       ├── analytics.py   # Analytics and insights endpoints
│   │       ├── notifications.py # Notification management
│   │       └── websockets.py  # WebSocket endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py         # Pydantic data models
│   │   ├── logsClassifier.py  # AI log classifier
│   │   ├── logsPreprocessor.py # Log preprocessing
│   │   ├── notificationModel.py # Notification logic
│   │   └── suggestionModel.py # AI suggestions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── log_processor.py   # Core log processing service
│   │   └── websocket_manager.py # WebSocket connection manager
│   └── types/
│       ├── __init__.py
│       ├── classifierTypes.py # Type definitions
│       └── suggestionTypes.py
└── logs/
    ├── dockerLogs.log
    └── exLogs.log
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Quick Install

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend/
   ```

2. **Install dependencies:**
   ```bash
   # Option 1: Use the installer script
   python install_deps.py
   
   # Option 2: Install manually
   pip install fastapi uvicorn[standard] websockets pydantic python-dotenv aiofiles
   
   # Option 3: Install from requirements
   pip install -r ../requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python test_backend.py
   ```

## 🚀 Quick Start

### 1. Start the Server

```bash
# Development server with auto-reload
python run_server.py

# Or manually
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Access the API

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs  
- **ReDoc**: http://localhost:8000/redoc
- **WebSocket**: ws://localhost:8000/api/ws/

### 3. Test Log Streaming

```bash
# Send a test log via curl
curl -X POST "http://localhost:8000/api/logs/stream/my-service" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "my-service",
    "logs": [
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "level": "ERROR",
        "message": "Database connection failed",
        "service": "my-service",
        "metadata": {"error_code": "DB_001"}
      }
    ]
  }'
```

## 📡 API Endpoints

### Log Management
- `POST /api/logs/stream/{service_name}` - Stream log batches
- `POST /api/logs/stream/{service_name}/single` - Stream single log
- `POST /api/logs/stream/{service_name}/continuous` - Continuous streaming
- `GET /api/logs/services` - List registered services
- `POST /api/logs/services/register` - Register new service

### Health Monitoring  
- `GET /api/health/` - System health overview
- `GET /api/health/services/{service_name}` - Service health details
- `GET /api/health/alerts` - Active alerts
- `POST /api/health/alerts/{alert_id}/acknowledge` - Acknowledge alert

### Analytics
- `POST /api/analytics/query` - Advanced log queries
- `GET /api/analytics/trends/{service_name}` - Service trends
- `GET /api/analytics/insights` - AI-generated insights
- `GET /api/analytics/errors/patterns` - Error pattern analysis

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
- `POST /api/notifications/bulk` - Bulk operations
- `GET /api/notifications/channels` - Notification channels

### WebSocket Endpoints
- `WS /api/ws/live` - Live updates (all)
- `WS /api/ws/health` - Health status updates
- `WS /api/ws/logs/{service_name}` - Service-specific logs
- `WS /api/ws/alerts` - Alert notifications

## ⚙️ Configuration

Create a `.env` file in the backend directory:

```env
# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=info

# Processing Configuration  
PROCESSING_INTERVAL_SECONDS=30
BATCH_SIZE=100
MAX_LOG_BATCH_SIZE=1000

# AI Configuration
GROQ_API_KEY=your_groq_api_key_here
AGNO_API_KEY=your_agno_api_key_here
AI_CLASSIFICATION_ENABLED=true

# WebSocket Configuration
MAX_WEBSOCKET_CONNECTIONS=100
WEBSOCKET_HEARTBEAT_INTERVAL=30

# Storage Paths
LOG_STORAGE_PATH=./logs
OUTPUT_STORAGE_PATH=./outputs
```

## 🔄 Real-time Processing

The backend processes logs in 30-second chunks:

1. **Log Ingestion**: Receives logs via HTTP endpoints
2. **Buffering**: Accumulates logs in memory buffers per service
3. **Batch Processing**: Processes accumulated logs every 30 seconds
4. **AI Classification**: Uses existing AI models for log analysis
5. **Health Updates**: Updates service health based on log patterns
6. **Real-time Updates**: Broadcasts updates via WebSocket

### Processing Pipeline

```python
# Example log processing flow
Log → Buffer → [30s] → AI Classifier → Health Analyzer → WebSocket Broadcast
```

## 🌐 WebSocket Integration

### Frontend Connection Example

```javascript
// Connect to live updates
const ws = new WebSocket('ws://localhost:8000/api/ws/live');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'log_processed':
      updateLogCount(data.data);
      break;
    case 'health_update':
      updateServiceHealth(data.data);
      break;
    case 'alert_triggered':
      showAlert(data.data);
      break;
  }
};

// Subscribe to specific service
ws.send(JSON.stringify({
  type: 'subscribe',
  subscription_type: 'service_logs',
  service_name: 'my-service'
}));
```

## 🔧 Development

### Running Tests

```bash
# Test backend structure
python test_backend.py

# Test API endpoints (requires server running)
curl http://localhost:8000/api/

# Test WebSocket connection
wscat -c ws://localhost:8000/api/ws/live
```

### Development Workflow

1. **Start development server:**
   ```bash
   python run_server.py
   ```

2. **Make changes** - Server auto-reloads with `--reload` flag

3. **Test endpoints** using the interactive docs at `/docs`

4. **Monitor logs** in the console output

### Adding New Features

1. **Models**: Add Pydantic schemas in `app/models/schemas.py`
2. **Routes**: Create new routes in `app/api/routes/`
3. **Services**: Add business logic in `app/services/`
4. **Configuration**: Update settings in `app/core/config.py`

## 🚨 Monitoring & Alerting

### Health Monitoring

The system continuously monitors:
- Log volume and patterns
- Error rates and types  
- Service availability
- Processing performance
- WebSocket connection health

### Alert Triggers

Alerts are triggered for:
- High error rates (>5% in 5 minutes)
- Service unavailability (no logs for 10 minutes)  
- Critical errors or exceptions
- Processing lag (>60 seconds)
- WebSocket connection issues

## 🔒 Security

- **Input Validation**: All inputs validated with Pydantic
- **Rate Limiting**: Configurable request rate limits
- **CORS**: Properly configured for frontend integration
- **Environment Variables**: Sensitive data in `.env` files
- **Error Handling**: Secure error responses without data leaks

## 📈 Performance

### Optimization Features

- **Async Processing**: Full async/await implementation
- **Batch Processing**: Efficient 30-second batch cycles
- **Connection Pooling**: WebSocket connection management
- **Memory Management**: Proper buffer management and cleanup
- **Background Tasks**: Non-blocking operations

### Scalability Considerations

- **Horizontal Scaling**: Stateless design for multiple instances
- **Database Integration**: Ready for external database backends
- **Caching**: Built-in support for Redis/memory caching
- **Load Balancing**: Compatible with reverse proxies

## 🚀 Deployment

### Production Setup

1. **Environment Variables:**
   ```env
   ENVIRONMENT=production
   DEBUG=false
   LOG_LEVEL=warning
   ```

2. **Process Manager:**
   ```bash
   # Using systemd
   sudo systemctl start logviewer-backend
   
   # Using PM2
   pm2 start run_server.py --name logviewer-backend
   ```

3. **Reverse Proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with the Next.js frontend:

- **CORS Configuration**: Allows frontend origin
- **WebSocket Support**: Real-time updates for dashboard
- **REST API**: Standard HTTP endpoints for data fetching
- **TypeScript Types**: Shared type definitions available

## 📚 API Documentation

Full API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Install missing dependencies with `pip install -r requirements.txt`
2. **Port Conflicts**: Change port in `run_server.py` or kill conflicting processes
3. **WebSocket Issues**: Check firewall settings and CORS configuration
4. **AI Model Errors**: Verify API keys in `.env` file

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=debug
python run_server.py
```

### Health Check

```bash
# Check if server is running
curl http://localhost:8000/api/status

# Test WebSocket
wscat -c ws://localhost:8000/api/ws/live
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly  
4. Submit a pull request

## 📄 License

This project is part of the LogViewer system. See the main project LICENSE file.

---

**🚀 Ready to stream logs in real-time!** 

Start the server with `python run_server.py` and visit http://localhost:8000/docs for interactive API documentation.
