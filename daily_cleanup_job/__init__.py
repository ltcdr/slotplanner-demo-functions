import logging
import azure.functions as func
import requests
import os


# Backend base URL – configurable via App Settings
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://slotplanner-demo-bmc4hpa9f7ccd6g3.westeurope-01.azurewebsites.net"
)


# ------------------------------------------------------------
# Daily Cleanup – every day at 03:00
# ------------------------------------------------------------
def main(myTimer: func.TimerRequest):
    logging.info("Daily cleanup job triggered.")

    if myTimer.past_due:
        logging.warning("Daily cleanup job is past due!")

    try:
        cleanup_url = f"{BACKEND_URL}/admin/cleanup_old"
        logging.info(f"Calling backend: POST {cleanup_url}")
        cleanup_response = requests.post(cleanup_url, timeout=30)

        logging.info(f"cleanup_old status: {cleanup_response.status_code}")
        logging.info(f"cleanup_old response: {cleanup_response.text}")

    except Exception as e:
        logging.error(f"Error during daily cleanup: {e}")
