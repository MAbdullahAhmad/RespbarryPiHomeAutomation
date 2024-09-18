import time
import RPi.GPIO as GPIO
from config.settings import PIR_PIN, DETECTION_COUNT_THRESHOLD, DETECTION_ON_WAIT, DEBUG
from lib.logs import log_info

class PIRController:
    def __init__(self):
        self.detect_count = 0
        self.motion_detected = False
        self.last_motion_time = 0
        self.last_off_detected = False

    def detect_motion(self):
        pir_read = GPIO.input(PIR_PIN)
        if DEBUG: log_info(f"PIR = {pir_read}")

        # Motion detected
        if pir_read:
            if self.detect_count < DETECTION_COUNT_THRESHOLD:
                self.detect_count += 1

            if self.detect_count >= DETECTION_COUNT_THRESHOLD and not self.motion_detected:
                self.motion_detected = True
                log_info("Motion detected")
                self.last_off_detected = False

        # No motion detected
        else:
            self.detect_count = 0
            if self.motion_detected and not self.last_off_detected:
                self.last_off_detected = True
                self.last_motion_time = time.time()
                log_info("Waiting to turn off motion detection...")

            if self.last_off_detected and (time.time() - self.last_motion_time >= DETECTION_ON_WAIT):
                self.motion_detected = False
                self.last_off_detected = False
                log_info("No motion detected, turning off detection")
