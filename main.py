import requests
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import time

BOT_TOKEN = "8717363540:AAEYs4DMNzXstTWhqwoqD4plofx7YfizmdQ"
CHAT_ID = "7383029478"

wallet = "0x7f50e3cd6c62a72dce3b356a6abe786572e963be"

bot = Bot(token=BOT_TOKEN)

last_trade = None

def check_wallet():
    global last_trade

    url = f"https://gamma-api.polymarket.com/trades?user={wallet}"
    r = requests.get(url)
    data = r.json()

    if not data:
        return

    trade = data[0]

    if trade["id"] != last_trade:
        last_trade = trade["id"]

        message = f"""
🚨 New Wallet Trade

Market: {trade['market']}
Side: {trade['side']}
Outcome: {trade['outcome']}
Amount: {trade['amount']}
Price: {trade['price']}
        """

        bot.send_message(chat_id=CHAT_ID, text=message)

scheduler = BackgroundScheduler()
scheduler.add_job(check_wallet, "interval", seconds=30)
scheduler.start()

while True:
    time.sleep(5)
