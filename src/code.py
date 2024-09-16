import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
PIR_PIN = 16  # GPIO pin for PIR sensor
LED_PIN = 17  # GPIO pin for LED

# Set up GPIO pins
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Main loop
try:
    print("Motion Detection System Initialized")
    while True:
        if GPIO.input(PIR_PIN):
            # Motion detected
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("Motion Detected! LED ON")
        else:
            # No motion
            GPIO.output(LED_PIN, GPIO.LOW)
            print("No Motion. LED OFF")
        time.sleep(0.1)  # Check every 100ms

except KeyboardInterrupt:
    print("Program terminated")
    GPIO.cleanup()
