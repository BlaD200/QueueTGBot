import logging

from telegram import Update, ParseMode, Bot
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from bot.config import BOT_TOKEN


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)


def setup():
    logging.info("Setup bot")
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Registering commands handlers here #

    # Registering conversation handlers here

    # Registering handlers here #
    start_message_handler = MessageHandler(Filters.all, start_handler)
    dispatcher.add_handler(start_message_handler)

    return dispatcher, updater


def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f"Hello, [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})!",
        parse_mode=ParseMode.MARKDOWN
    )


def test_server():
    logging.info('Started server with polling')
    # Do NOT USE it in a production deployment.
    # for PRODUCTION use WEBHOOK
    _, updater = setup()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    test_server()
