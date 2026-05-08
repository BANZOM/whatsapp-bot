import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_PHONE = sys.argv[1] if len(sys.argv) > 1 else os.getenv("RECIPIENT_PHONE")

url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

data = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "template",
    "template": {"name": "hello_world", "language": {"code": "en_US"}},
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.json())
