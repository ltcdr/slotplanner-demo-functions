import logging
import azure.functions as func
import requests
import os

app = func.FunctionApp()

# Backend base URL – configurable via App Settings
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://slotplanner-demo-bmc4hpa9f7ccd6g3.westeurope-01.azurewebsites.net"
)

# ------------------------------------------------------------
# Weekly Activity Creation – every Friday at 06:00
# ------------------------------------------------------------
@app.timer_trigger(
    schedule="0 0 6 * * 5",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def weekly_activity_job(myTimer: func.TimerRequest) -> None:
    logging.info("Weekly activity job triggered.")

    if myTimer.past_due:
        logging.warning("Weekly job is past due!")

    try:
        # 1. Generate next week's activities
        gen_url = f"{BACKEND_URL}/demo/admin/generate_next_week"
        logging.info(f"Calling backend: POST {gen_url}")
        gen_response = requests.post(gen_url, timeout=30)

        logging.info(f"generate_next_week status: {gen_response.status_code}")
        logging.info(f"generate_next_week response: {gen_response.text}")

        # 2. Clean up old activities
        cleanup_url = f"{BACKEND_URL}/demo/admin/cleanup_old"
        logging.info(f"Calling backend: POST {cleanup_url}")
        cleanup_response = requests.post(cleanup_url, timeout=30)

        logging.info(f"cleanup_old status: {cleanup_response.status_code}")
        logging.info(f"cleanup_old response: {cleanup_response.text}")

    except Exception as e:
        logging.error(f"Error during weekly automation: {e}")


# ------------------------------------------------------------
# Daily Cleanup – every day at 03:00
# ------------------------------------------------------------
@app.timer_trigger(
    schedule="0 0 3 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def daily_cleanup_job(myTimer: func.TimerRequest) -> None:
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
