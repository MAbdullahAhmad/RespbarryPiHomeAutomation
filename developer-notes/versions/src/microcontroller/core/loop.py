import time
from controllers.PIRController import PIRController
from controllers.RelayController import RelayController
from controllers.APIController import APIController
from controllers.LDRController import LDRController

# Controllers
pir_controller = PIRController()
relay_controller = RelayController()
api_controller = APIController()
ldr_controller = LDRController()

# Loop
def run_loop():
    # Fetch device modes from the Flask API
    device_modes = api_controller.fetch_device_modes()

    # Check PIR sensor
    pir_controller.detect_motion()

    # Read LDR Value
    ldr_controller.detect_light()

    # Mode Loop
    if device_modes:
        for device, mode in device_modes.items():

            # Mode: On/Off
            if   mode == 'on':  relay_controller.turn_on(device)
            elif mode == 'off': relay_controller.turn_off(device)

            # Mode: Motion
            elif mode == 'motion':
                if pir_controller.motion_detected: relay_controller.turn_on(device)
                else:                              relay_controller.turn_off(device)
            
            # Mode: Ambient
            elif mode == 'ambient':
                if ldr_controller.is_dark(): relay_controller.turn_on(device)
                else:                        relay_controller.turn_off(device)
    
    # Small sleep between loops
    time.sleep(0.1)
