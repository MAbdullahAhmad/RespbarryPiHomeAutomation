from util.get_ip import get_ip

# GPIO pin configuration
PIR_PIN = 25
RELAY_PINS = {
    'bulb': 23,
    'fan': 24,
}

LDR_PIN = 16


# Server configuration
SERVER_HOST = f'http://{get_ip()}:8000/sync' or 'http://127.0.0.1:8000/sync'

# Motion Detection constants
DETECTION_COUNT_THRESHOLD = 3
DETECTION_ON_WAIT = 10

# Debug Mode
DEBUG = False
