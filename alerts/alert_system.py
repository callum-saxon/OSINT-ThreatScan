import requests
import logging

logging.basicConfig(level=logging.INFO)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1338345507046822041/WX6whV2qGSCOEwNbDnlz-BbTESwcg0NOKjrNQrf0ODX5V1LjggLlk6eg3ZMJbkc8qRF-"

def send_discord_alert(subject, body):

    payload = {
        "content": f"**ALERT:** {subject}\n{body}"
    }
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        resp.raise_for_status()
        logging.info("Alert posted to Discord.")
    except Exception as e:
        logging.error(f"Could not send Discord alert: {e}")
