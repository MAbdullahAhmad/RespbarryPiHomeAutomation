import time
import RPi.GPIO as GPIO
from config.settings import PIR_PIN, DETECTION_COUNT_THRESHOLD, DETECTION_ON_WAIT, DEBUG
from lib.logs import log_info

motion_detected = 0  # Global motion detection state
current_count = 0    # To keep track of current detection counts

class PIRController:
    def __init__(self):
        self.current_detected = 0
        self.last_off_detected = False
        self.last_off_time = 0

    def detect_motion(self):
        global motion_detected, current_count

        pir_read = GPIO.input(PIR_PIN)
        if DEBUG: log_info(f"PIR = {pir_read}")

        # If device has motion detected
        if pir_read:
            if self.current_detected <= DETECTION_COUNT_THRESHOLD:
                self.current_detected += 1

                # If detected 3 times constantly
                if self.current_detected >= DETECTION_COUNT_THRESHOLD:

                    # Update Motion detected
                    if not motion_detected:
                        motion_detected = 1
                        log_info("Motion detected")

                    # set threshold
                    current_count = DETECTION_COUNT_THRESHOLD
                    self.last_off_detected = False

        # If device has motion state "not detected"
        else:
            self.current_detected = 0

            # Start waiting for time threshold
            if motion_detected and not self.last_off_detected:
                self.last_off_detected = True
                self.last_off_time = time.time()
                log_info("Waiting to turn off motion detection...")

            if self.last_off_detected:
                elapsed_time = time.time() - self.last_off_time

                # If threshold reaches
                if elapsed_time >= DETECTION_ON_WAIT:
                    motion_detected = 0
                    self.last_off_detected = False
                    log_info("No motion detected, turning off detection")
