import requests

BOT_TOKEN = "1234567890:ABCdefGhIjklMNOpQrSTUVwxyz1234567890"
CHAT_ID = "98*****1"
MESSAGE = "⚠️ Linux system is shutting down!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
requests.get(url)
