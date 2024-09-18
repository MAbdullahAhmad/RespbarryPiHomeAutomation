import RPi.GPIO as GPIO
from config.settings import LDR_PIN, DARKNESS_THRESHOLD
from lib.logs import log_info

DEBUG_LDR = True

class LDRController:
    ldr_value = 0

    def detect_light(self):
        self.ldr_value = GPIO.input(LDR_PIN)

        # Debug
        if DEBUG_LDR: log_info("LDR = ", self.ldr_value)

        return self.ldr_value
    
    def is_dark(self):
        return self.ldr_value < DARKNESS_THRESHOLD
