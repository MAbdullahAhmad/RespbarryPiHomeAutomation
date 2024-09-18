# controllers/APIController.py
import requests
from config.settings import SERVER_HOST
from controllers.LogsController import log_info, log_error

class APIController:
    def fetch_device_modes(self):
        try:
            response = requests.get(SERVER_HOST)
            if response.status_code == 200:
                log_info("Successfully fetched device modes.")
                return response.json()
            else:
                log_error(f"Failed to fetch device modes: {response.status_code}")
                return None
        except Exception as e:
            log_error(f"Error fetching device modes: {str(e)}")
            return None
