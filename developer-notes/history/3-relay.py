import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for relays
relay_pins = [23, 24, 25, 16, 5, 6]

# Set up GPIO pins for relays
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all relays are off initially

def turn_on_relay(channel):
    GPIO.output(relay_pins[channel], GPIO.HIGH)
    print(f"Relay {channel + 1} ON")

def turn_off_relay(channel):
    GPIO.output(relay_pins[channel], GPIO.LOW)
    print(f"Relay {channel + 1} OFF")

def main():
    try:
        while True:
            command = input("Enter command (e.g., 'on 1', 'off 2', 'exit'): ")
            parts = command.split()
            if len(parts) != 2:
                print("Invalid command. Use format 'on <relay_number>' or 'off <relay_number>'")
                continue

            action, relay_number = parts
            if not relay_number.isdigit():
                print("Invalid relay number. Must be a number between 1 and 6.")
                continue

            relay_number = int(relay_number) - 1
            if relay_number < 0 or relay_number > 5:
                print("Relay number out of range. Must be between 1 and 6.")
                continue

            if action == 'on':
                turn_on_relay(relay_number)
            elif action == 'off':
                turn_off_relay(relay_number)
            elif action == 'exit':
                break
            else:
                print("Invalid action. Use 'on', 'off', or 'exit'.")
                
    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
