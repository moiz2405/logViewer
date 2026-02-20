# myApp - Multi-Service FastAPI Demo

A complete example showing how to integrate the Sentry SDK with a FastAPI application.

---

## 🎯 What This Demonstrates

- ✅ SDK integration with FastAPI
- ✅ Multiple microservices (API, Auth, Inventory, Payment, Notification)
- ✅ Different log levels (INFO, WARNING, ERROR)
- ✅ Service health monitoring
- ✅ Bad log ratio simulation
- ✅ Docker deployment
- ✅ Environment variable configuration

---

## 🏗️ Architecture

```
myApp (FastAPI :8000)
  ├── API Service       (handles HTTP requests)
  ├── Auth Service      (user authentication)
  ├── Inventory Service (stock management)
  ├── Payment Service   (transactions)
  └── Notification Service (alerts)
  
Each service generates logs → Sentry SDK → Backend → Dashboard
```

---

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# 1. Get API key from dashboard
# Visit http://localhost:3000/register → Create app → Copy API key

# 2. Install dependencies
pip install -r requirements.txt
pip install ../../sdk/python

# 3. Set environment variables
export SENTRY_API_KEY=sk_abc123xyz...
export SENTRY_DSN=http://localhost:8001

# 4. Run the app
python main.py

# 5. View logs at http://localhost:3000
```

### Option 2: Run with Docker

```bash
# 1. Build image
docker build -t myapp-demo .

# 2. Run container
docker run -p 8000:8000 \
  -e SENTRY_API_KEY=your-api-key \
  -e SENTRY_DSN=http://host.docker.internal:8001 \
  myapp-demo

# 3. View logs at http://localhost:3000
```

### Option 3: Use Docker Compose (from root)

```bash
# From project root directory
cd ../..

# 1. Create docker-compose.override.yml
cat > docker-compose.override.yml << 'EOF'
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key-here
EOF

# 2. Start all services
docker-compose up -d

# 3. View logs at http://localhost:3000
```
- **Inventory Service**: Simulates inventory management operations
- **Notification Service**: Simulates various notification deliveries
- **Payment Service**: Simulates payment processing workflows

## Usage

### Starting the Services

Run the system with the default bad log ratios (2 out of 10 logs are errors/warnings for each service):

```bash
python main.py
```

To customize the bad log ratio for each service individually (0-10, where 0 means no bad logs and 10 means all logs are bad):

```bash
python main.py --api-ratio 3 --auth-ratio 1 --inventory-ratio 5 --notification-ratio 2 --payment-ratio 4
```

### Changing Bad Ratios at Runtime

You can update the bad log ratios for any service while the system is running, without having to restart.

#### Using the update_ratios tool

```bash
# Get current ratios
python tools/update_ratios.py --get

# Update specific services
python tools/update_ratios.py --api 8 --payment 7

# Update all services
python tools/update_ratios.py --api 1 --auth 2 --inventory 3 --notification 4 --payment 5
```

#### From your own Python code

```python
from tools.update_ratios import update_ratios, get_current_ratios

# Get current ratios
current = get_current_ratios()
print(current)

# Update API and Payment services, leave others unchanged
update_ratios(api=7, payment=9)
```

## Log Types

Each service produces a variety of log types:

- **INFO**: Normal operation logs
- **DEBUG**: Detailed information useful for debugging
- **WARNING**: Potential issues that don't cause failures
- **ERROR**: Failed operations or system errors

## Examples

Generate logs with a low error rate for API service but high for Payment service:

```bash
python main.py --api-ratio 1 --payment-ratio 8
```

Start with all services having moderate error rates, then increase API errors during runtime:

```bash
# Start services
python main.py

# Later, increase API errors
python tools/update_ratios.py --api 8
```

## Log Format

Logs are written to both the console and the `app.log` file with the following format:

```
timestamp [LEVEL] [ServiceName]: Message
```
