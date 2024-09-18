# core/loop.py
import time
from controllers.PIRController import PIRController
from controllers.RelayController import RelayController
from controllers.APIController import APIController

# Controllers
pir_controller = PIRController()
relay_controller = RelayController()
api_controller = APIController()

# Loop
def run_loop():
    # Fetch device modes from the Flask API
    device_modes = api_controller.fetch_device_modes()

    # Check PIR sensor
    pir_controller.detect_motion()

    # Mode Loop
    if device_modes:
        for device, mode in device_modes.items():

            # Mode = On
            if mode == 'on':
                relay_controller.turn_on(device)

            # Mode = Off
            elif mode == 'off':
                relay_controller.turn_off(device)

            # Mode = Motion
            elif mode == 'motion':
                if pir_controller.motion_detected: relay_controller.turn_on(device)
                else:                              relay_controller.turn_off(device)


    
    time.sleep(0.1)  # Small sleep between loops
