# MQTT Data Service

A Python service that collects real-time data from MQTT broker and provides REST API access.

## Features
- Subscribe to MQTT topics
- Store latest received data
- REST API endpoint to access data
- Configurable MQTT broker and topic

## Requirements
- Python 3.7+
- See requirements.txt for dependencies

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit config.py to set:
- MQTT broker address
- MQTT topic
- Web service port

## Running the Service
```bash
python main.py
```

The service will:
1. Connect to MQTT broker
2. Start web server on port 8000

## API Endpoints
- GET / - Service status
- GET /data - Get latest received data

## Testing
Publish test data to the configured MQTT topic:
```bash
mosquitto_pub -h broker.hivemq.com -t sensors/data -m '{"temperature": 25.5}'
```

Then access:
http://localhost:8000/data
