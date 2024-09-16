import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO 17 (pin 11) for LED output
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

# Blink the LED
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
        print("LED is ON")
        time.sleep(1)  # Wait for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off the LED
        print("LED is OFF")
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()  # Clean up all the GPIO pins
