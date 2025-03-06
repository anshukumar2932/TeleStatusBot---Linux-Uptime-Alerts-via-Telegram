import requests
import time
import os

BOT_TOKEN = "1234567890:ABCdefGhIjklMNOpQrSTUVwxyz1234567890"
CHAT_ID = "98*****1"
MESSAGE = f"🔔 Linux system is online! {time.ctime()}"

# Wait for network connectivity before sending a message (max 50 seconds)
for _ in range(10):  # Try for 50 seconds (10 tries x 5 sec)
    try:
        requests.get("https://api.telegram.org", timeout=5)
        break  # Exit loop if network is available
    except requests.exceptions.RequestException:
        time.sleep(5)  # Wait 5 seconds before retrying

# ✅ Send message to Telegram **once**
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": MESSAGE}
response = requests.get(url, params=params)

# ✅ Log response (optional)
with open("/home/anshu/telegram_log.txt", "a") as log:
    log.write(f"{time.ctime()}: {response.status_code} - {response.text}\n")
