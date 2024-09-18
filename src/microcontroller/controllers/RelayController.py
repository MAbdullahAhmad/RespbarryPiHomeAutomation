# controllers/RelayController.py
import RPi.GPIO as GPIO
from config.settings import RELAY_PINS
from lib.logs import log_info

class RelayController:
    def turn_on(self, device):
        if device in RELAY_PINS:
            GPIO.output(RELAY_PINS[device], GPIO.HIGH)
            log_info(f"Relay for {device} ON")

    def turn_off(self, device):
        if device in RELAY_PINS:
            GPIO.output(RELAY_PINS[device], GPIO.LOW)
            log_info(f"Relay for {device} OFF")
