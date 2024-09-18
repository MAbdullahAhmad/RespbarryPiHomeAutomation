# config/settings.py

# GPIO pin configuration
PIR_PIN = 25
RELAY_PINS = {
    'bulb': 23,
    'fan': 24,
}

# Server configuration
SERVER_HOST = 'http://your-flask-server/sync'

# Detection constants
DETECTION_COUNT_THRESHOLD = 3
DETECTION_ON_WAIT = 10  # seconds
