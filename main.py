# Copyright (C) 2021 Vladyslav Synytsyn

import json
import logging
from urllib.request import urlopen

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher

import app_logging
from bot.constants import WEBHOOK_URL, BOT_TOKEN
from bot.setup_bot import *


app = Flask(__name__)

# Declaring a global dispatcher
dispatcher: Dispatcher

# Registering logger here
logger: logging.Logger = app_logging.get_logger(__name__)


@app.route("/", methods=["GET", "HEAD"])
def index():
    return '<h1>Telegram Bot by <a href="tg://user?id=386151408">Vlad Synytsyn</a></h1>'


@app.route('/', methods=['Post'])
def webhook():
    json_request = request.get_json()
    update = telegram.Update.de_json(json_request, dispatcher.bot)
    dispatcher.process_update(update)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# if __name__ == '__main__':
# Check, if bot correctly connect to Telegram API
info = bot.get_me()
logger.info(f'Bot info: {info}')
logger.info(bot.get_webhook_info())

if bot.get_webhook_info()['url'] != WEBHOOK_URL:
    urlopen(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')

logger.info(bot.get_webhook_info())

dispatcher, _ = setup()
logger.info('Started server with webhook')
