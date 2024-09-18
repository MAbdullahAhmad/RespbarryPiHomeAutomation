import RPi.GPIO as GPIO
from config.settings import RELAY_PINS
from lib.logs import log_info

class RelayController:
    def __init__(self):
        # Store the previous states of the devices
        self.device_states = {device: None for device in RELAY_PINS}

    def turn_on(self, device):
        if device in RELAY_PINS:
            # Check if the state is already ON, if not, change it and log
            if self.device_states[device] != 'ON':
                GPIO.output(RELAY_PINS[device], GPIO.LOW)
                self.device_states[device] = 'ON'
                log_info(f"Relay for {device} ON")

    def turn_off(self, device):
        if device in RELAY_PINS:
            # Check if the state is already OFF, if not, change it and log
            if self.device_states[device] != 'OFF':
                GPIO.output(RELAY_PINS[device], GPIO.HIGH)
                self.device_states[device] = 'OFF'
                log_info(f"Relay for {device} OFF")
