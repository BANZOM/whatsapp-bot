# WhatsApp Bot

Send WhatsApp messages using the [WhatsApp Business Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api).

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` or create a `.env` file:

```
PHONE_NUMBER_ID=your_phone_number_id
ACCESS_TOKEN=your_access_token
RECIPIENT_PHONE=recipient_number_with_country_code
```

## Usage

```bash
python send_message.py
```

This sends the default `hello_world` template message to the configured recipient.
