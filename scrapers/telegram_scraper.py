import logging

logging.basicConfig(level=logging.INFO)

def scrape_telegram_channel(channel_id="@examplechannel", limit=5):

    # Return mock data for demonstration
    messages_data = []
    for i in range(limit):
        messages_data.append({
            "source": "telegram",
            "channel": channel_id,
            "content": f"Mock Telegram message {i}"
        })
    return messages_data
