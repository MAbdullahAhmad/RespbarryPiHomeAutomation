# main.py
import time
from core.setup import setup_gpio
from core.loop import run_loop
from lib.logs import log_info

def main():
    setup_gpio()
    
    time.sleep(2)  # Initial 2-second delay before starting

    try:
        while True:
            run_loop()  # Main loop logic from loop.py
    except KeyboardInterrupt:
        log_info("Program terminated.")
    finally:
        import RPi.GPIO as GPIO
        GPIO.cleanup()

if __name__ == "__main__":
    main()
