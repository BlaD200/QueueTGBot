from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from bot.command_handlers import *
from bot.config import BOT_TOKEN


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)


def setup():
    """
    Setting up updater.

    Registered all handlers (for commands)

    Returns:
        dispatcher and updater
    """
    logging.info("Setup bot")
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Registering commands handlers here #
    dispatcher.add_handler(CommandHandler('start', start_command))

    dispatcher.add_handler(CommandHandler('create_queue', create_queue_command))
    dispatcher.add_handler(CommandHandler('delete_queue', delete_queue_command))
    dispatcher.add_handler(CommandHandler('show_queues', show_queues_command))
    dispatcher.add_handler(CommandHandler('notify_all', unimplemented_command_handler))

    dispatcher.add_handler(CommandHandler('add_me', unimplemented_command_handler))
    dispatcher.add_handler(CommandHandler('remove_me', unimplemented_command_handler))
    dispatcher.add_handler(CommandHandler('skip_me', unimplemented_command_handler))
    dispatcher.add_handler(CommandHandler('next', unimplemented_command_handler))

    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('about_me', about_me_command))

    # Registering conversation handlers here

    # Registering handlers here #
    dispatcher.add_handler(MessageHandler(Filters.command, unsupported_command_handler))
    dispatcher.add_handler(MessageHandler(Filters.all, unsupported_command_handler))

    return dispatcher, updater


def test_server():
    """
    Starting bot with polling (without webhook).

    Note:
        Don't use this for production.
    """
    logging.info('Started server with polling')
    # Do NOT USE it in a production deployment.
    # for PRODUCTION use WEBHOOK
    _, updater = setup()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    test_server()
