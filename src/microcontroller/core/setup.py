# core/setup.py
import RPi.GPIO as GPIO
from config.settings import RELAY_PINS, PIR_PIN

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    
    # Set up relay pins
    for pin in RELAY_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Ensure all relays are off initially
    
    # Set up PIR pin
    GPIO.setup(PIR_PIN, GPIO.IN)

    print("GPIO setup complete.")
