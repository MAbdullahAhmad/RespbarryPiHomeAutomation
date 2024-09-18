# config/settings.py
from util.get_ip import get_ip

# GPIO pin configuration
PIR_PIN = 25
RELAY_PINS = {
    'bulb': 23,
    'fan': 24,
}

# Server configuration
SERVER_HOST = f'http://{get_ip()}/sync' or 'http://127.0.0.1:8000/sync'

# Detection constants
DETECTION_COUNT_THRESHOLD = 3
DETECTION_ON_WAIT = 10  # seconds

DEBUG = False
