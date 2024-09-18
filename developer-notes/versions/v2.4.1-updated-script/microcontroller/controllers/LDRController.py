import RPi.GPIO as GPIO
from config.settings import LDR_PIN
from lib.logs import log_info

DEBUG_LDR = False

class LDRController:
    ldr_value = 0

    def detect_light(self):
        self.ldr_value = GPIO.input(LDR_PIN)

        # Debug
        if DEBUG_LDR: log_info("LDR = ", self.ldr_value)

        return self.ldr_value
    
    def is_dark(self):
        return bool(self.ldr_value)
