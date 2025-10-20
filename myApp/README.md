# Demo Backend Log Generator

This project simulates a production backend system with multiple services generating realistic logs. It's designed to produce a mixture of normal logs and error logs with configurable ratios for each service.

## Services

The system includes the following services:

- **API Service**: Simulates REST API requests and responses
- **Auth Service**: Simulates user authentication flows
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
