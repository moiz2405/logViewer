# 📚 Example Applications

This directory contains example applications that demonstrate how to integrate the Sentry SDK.

---

## 🗂️ Available Examples

### 1. **myApp** - Multi-Service FastAPI Demo

**Location:** `examples/myApp/`

A complete FastAPI application with multiple microservices that demonstrates:
- ✅ SDK integration with FastAPI
- ✅ Multiple services (API, Auth, Inventory, Payment, Notification)
- ✅ Different log levels and patterns
- ✅ Docker deployment
- ✅ Environment variable configuration

**How to run:**
```bash
cd examples/myApp

# Option 1: Run locally
pip install -r requirements.txt
pip install ../../sdk/python
export SENTRY_API_KEY=your-api-key
export SENTRY_DSN=http://localhost:8001
python main.py

# Option 2: Run with Docker
docker build -t myapp-demo .
docker run -p 8000:8000 \
  -e SENTRY_API_KEY=your-api-key \
  -e SENTRY_DSN=http://host.docker.internal:8001 \
  myapp-demo
```

---

## 🚀 Quick Start for Any Example

### Step 1: Get API Key

1. Visit http://localhost:3000 (or your hosted instance)
2. Login with Google
3. Click "Add App" → Enter app name → Copy API key

### Step 2: Set Environment Variables

```bash
export SENTRY_API_KEY=sk_abc123xyz...
export SENTRY_DSN=http://localhost:8001  # or https://logs.yourapp.com
```

### Step 3: Run the Example

```bash
cd examples/<example-name>
pip install -r requirements.txt
python main.py
```

### Step 4: View Logs

- Go to http://localhost:3000
- Select your app from sidebar
- See logs in real-time!

---

## 📝 Creating Your Own Example

Want to add a new example? Here's the template:

```
examples/
  my-new-example/
    main.py           # Your app code
    requirements.txt  # Dependencies (include sentry-logger)
    README.md         # How to run
    .env.example      # Example env vars
    Dockerfile        # Optional
```

**Minimal example:**

```python
# main.py
from sentry_logger import init
import logging
import os

# Initialize SDK
init(
    api_key=os.getenv("SENTRY_API_KEY"),
    dsn=os.getenv("SENTRY_DSN", "http://localhost:8001")
)

# Your app code
logging.info("App started")
logging.warning("This is a warning")
logging.error("This is an error")
```

**requirements.txt:**
```txt
sentry-logger  # or -e ../../sdk/python for local dev
```

**README.md:**
```markdown
# My Example App

## Setup
1. Get API key from dashboard
2. Set environment variables:
   ```
   export SENTRY_API_KEY=your-key
   export SENTRY_DSN=http://localhost:8001
   ```
3. Run: `python main.py`
```

---

## 🎯 Example Categories

### Basic Examples
- [ ] Simple Python script
- [ ] Flask app
- [ ] Django app

### Framework Examples
- [x] FastAPI (see `myApp/`)
- [ ] Sanic
- [ ] Tornado

### Deployment Examples
- [x] Docker (see `myApp/`)
- [ ] Kubernetes
- [ ] AWS Lambda

### Advanced Examples
- [ ] Microservices architecture
- [ ] Distributed tracing
- [ ] Custom log formatters

---

## 🤝 Contributing Examples

Want to contribute an example?

1. Fork the repo
2. Create a new directory under `examples/`
3. Add your example with documentation
4. Test it works with the SDK
5. Submit a PR

**Guidelines:**
- Keep it simple and focused
- Include a README with clear instructions
- Use environment variables for API keys
- Add comments explaining key concepts
- Test before submitting

---

## 📚 More Resources

- [DEVELOPER_JOURNEY.md](../DEVELOPER_JOURNEY.md) - Complete integration guide
- [SDK-USAGE.md](../SDK-USAGE.md) - SDK API reference
- [START_HERE.md](../START_HERE.md) - Quick start guide

---

**Questions?** Open an issue or check the main docs! 🎉
