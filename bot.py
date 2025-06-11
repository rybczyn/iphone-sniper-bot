import requests
import time
import json
import threading
from flask import Flask

# ---- Discord config
with open("config.json") as f:
    config = json.load(f)

WEBHOOK_URL = config["discord_webhook"]
KEYWORDS = config["keywords"]
PRICE_MIN = config["price_min"]
PRICE_MAX = config["price_max"]
CHECK_INTERVAL = config["check_interval"]

already_sent = set()

# ---- Bot logic
def send_to_discord(title, url, image):
    data = {
        "embeds": [{
            "title": title,
            "url": url,
            "image": {"url": image}
        }]
    }
    requests.post(WEBHOOK_URL, json=data)

def check_vinted():
    try:
        for keyword in KEYWORDS:
            url = f"https://www.vinted.pl/api/v2/catalog/items?search_text={keyword}&price_from={PRICE_MIN}&price_to={PRICE_MAX}&currency=PLN&order=newest_first&per_page=20"
            response = requests.get(url, timeout=10)
            items = response.json().get("items", [])

            for item in items:
                item_id = item["id"]
                if item_id in already_sent:
                    continue
                title = item["title"]
                link = f"https://www.vinted.pl{item['url']}"
                image = item["photos"][0]["url"]
                send_to_discord(title, link, image)
                already_sent.add(item_id)
    except Exception as e:
        print(f"Błąd: {e}")

def run_bot():
    while True:
        check_vinted()
        time.sleep(CHECK_INTERVAL)

# ---- Dummy Flask app to keep Render alive
app = Flask(__name__)

@app.route('/')
def home():
    return "iPhone Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)

