import logging

import requests
from django.conf import settings


def send_telegram_message(chat_id, text):

    if not settings.TELEGRAM_BOT_TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN не задан в настройках")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()

        if result.get("ok"):
            return True
        else:
            error_msg = result.get("description", "Unknown error")
            logging.error(f"Ошибка Telegram API: {error_msg}")
            return False

    except requests.RequestException as e:
        logging.error(f"Ошибка сети при отправке в Telegram: {e}")
        return False
