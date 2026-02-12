import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def ask_openai(user_message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a Russian language teacher. Correct mistakes and explain simply."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    if "choices" not in result:
        return f"OpenAI error: {result}"

    return result["choices"][0]["message"]["content"]


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" not in data:
        return "ok"

    if "text" not in data["message"]:
        return "ok"

    message = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]

    reply = ask_openai(message)

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return "ok"


if __name__ == "__main__":
    app.run()
