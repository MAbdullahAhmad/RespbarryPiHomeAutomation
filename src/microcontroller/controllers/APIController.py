import requests
from config.settings import SERVER_HOST, DEBUG
from lib.logs import log_info, log_error

class APIController:
    def fetch_device_modes(self):
        try:
            response = requests.get(SERVER_HOST)
            if response.status_code == 200:
                if DEBUG: log_info("Successfully fetched device modes.")

                devices = response.json()
                device_modes = {device['label']: device['status'] for device in devices}
                
                return device_modes
            
            else:
                log_error(f"Failed to fetch device modes: {response.status_code}")
                return None
        except Exception as e:
            log_error(f"Error fetching device modes: {str(e)}")
            return None
