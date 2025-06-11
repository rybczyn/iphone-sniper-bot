import requests
import json
from flask import Flask
import threading

with open("config.json") as f:
    config = json.load(f)

WEBHOOK_URL = config["discord_webhook"]

def send_test():
    data = {
        "embeds": [{
            "title": "✅ Test powiadomienia",
            "description": "Bot działa i potrafi wysyłać wiadomości na Discord 🎯",
            "color": 3066993
        }]
    }
    response = requests.post(WEBHOOK_URL, json=data)
    print("Status:", response.status_code)

# Start test + dummy Flask for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot działa."

if __name__ == "__main__":
    threading.Thread(target=send_test).start()
    app.run(host="0.0.0.0", port=10000)
