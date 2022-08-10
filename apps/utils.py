import random
import string
import threading

import requests


def get_random_string(length: int = 32):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def _telegram_bot_sendtext(bot_message, tele_url, chat_id, token):
    send_text = "chat_id={chat_id}&parse_mode=HTML&text={msg}".format(chat_id=chat_id, msg=bot_message)
    url = tele_url.format(token=token)
    send_url = "{url}?{send_text}".format(url=url, send_text=send_text)
    response = requests.get(send_url)
    return response.json()


def telegram_bot_sendtext(bot_message, tele_url, chat_id, token, tag=None):

    if tag:
        bot_message = "[{tag}] - {message}".format(tag=tag, message=bot_message)
    t = threading.Thread(target=_telegram_bot_sendtext, args=(bot_message, tele_url, chat_id, token))
    t.start()
