"""In this module defined setup function, that is needed to configure bot before startup."""

import logging

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from bot.chat_status_handlers import (
    new_group_member_handler, left_group_member_handler, group_migrated_handler,
    new_group_created_handler
)
from bot.command_handlers import (
    start_command,
    create_queue_command,
    delete_queue_command,
    show_queues_command,
    help_command,
    about_me_command,
    unimplemented_command_handler,
    unsupported_command_handler, add_me_command, remove_me_command, skip_me_command, next_command, notify_all_command
)
from bot.config import BOT_TOKEN
from sql import get_tables, get_database_revision


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)


def setup():
    """
    Setting up updater.
    Checking the connectivity with the database.

    Registered all handlers (for commands)

    Returns:
        dispatcher and updater
    """
    logger.info(f"\n\tDB revision: {get_database_revision()}; \n\ttables: {get_tables()}")

    logging.info("Setting up bot...")
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Registering commands handlers here #
    dispatcher.add_handler(CommandHandler('start', start_command))

    dispatcher.add_handler(CommandHandler('create_queue', create_queue_command))
    dispatcher.add_handler(CommandHandler('delete_queue', delete_queue_command))
    dispatcher.add_handler(CommandHandler('show_queues', show_queues_command))
    dispatcher.add_handler(CommandHandler('notify_all', notify_all_command))

    dispatcher.add_handler(CommandHandler('add_me', add_me_command))
    dispatcher.add_handler(CommandHandler('remove_me', remove_me_command))
    dispatcher.add_handler(CommandHandler('skip_me', skip_me_command))
    dispatcher.add_handler(CommandHandler('next', next_command))
    dispatcher.add_handler(CommandHandler('show_members', unimplemented_command_handler))

    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('about_me', about_me_command))

    # Registering conversation handlers here

    # Registering handlers here #

    # Handlers for adding to a group, removing from a group, creating a new group with the bot in it
    # and updating the group to the supergroup
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_group_member_handler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_group_member_handler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.migrate, group_migrated_handler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.chat_created, new_group_created_handler))

    # Handlers for unsupported messages and commands.
    dispatcher.add_handler(MessageHandler(Filters.command, unsupported_command_handler))
    dispatcher.add_handler(MessageHandler(Filters.all, unexpected_message))

    return dispatcher, updater


# noinspection PyUnusedLocal
def unexpected_message(update: Update, context: CallbackContext):
    logger.info(f"unexpected message: [chat_id: {update.effective_chat.id}; message: {update.effective_message.text}]")
    pass


def test_server():
    """
    Starting bot with polling (without webhook).

    Note:
        Don't use this for production.
    """
    logging.info('Starting server with polling')
    # Do NOT USE it in a production deployment.
    # for PRODUCTION use WEBHOOK
    _, updater = setup()
    updater.start_polling()
    updater.idle()


__all__ = [
    'setup',
    'bot'
]

if __name__ == '__main__':
    test_server()
