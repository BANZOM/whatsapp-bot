import os
import requests as req
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secret_token")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

ai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_ai_reply(user_message):
    """Get a reply from AI via OpenRouter."""
    try:
        response = ai.chat.completions.create(
            model=os.getenv("AI_MODEL", "google/gemma-4-26b-a4b-it:free"),
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep replies short and conversational."},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI error: {e}")
        return "Sorry, I'm a bit busy right now. Please try again in a moment! 🙏"


def send_reply(to, text):
    """Send a text message reply."""
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    resp = req.post(url, headers=headers, json=data)
    print(f"Reply to {to}: {resp.status_code}")


@app.route("/webhook", methods=["GET"])
def verify():
    """Meta webhook verification."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive incoming messages and auto-reply."""
    data = request.get_json()

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            if "messages" not in value:
                continue
            for message in value.get("messages", []):
                phone = message["from"]
                msg_type = message["type"]
                text = message.get("text", {}).get("body", "")
                print(f"[{msg_type}] From {phone}: {text}")

                if msg_type == "text" and text:
                    reply = get_ai_reply(text)
                    send_reply(phone, reply)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
