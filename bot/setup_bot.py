"""In this module defined setup function, that is needed to configure bot before startup."""

import logging

from telegram import Bot, Update, BotCommand
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, ConversationHandler

import app_logging
from bot.constants import BOT_TOKEN, BOT_VERSION
from bot.handlers.chat_status_handlers import (
    new_group_member_handler, left_group_member_handler, group_migrated_handler,
    new_group_created_handler
)
from bot.handlers.command_handlers import (
    start_command,
    create_queue_command,
    delete_queue_command,
    show_queues_command,
    help_command,
    about_me_command,
    unsupported_command_handler, add_me_command, remove_me_command, skip_me_command, next_command, notify_all_command,
    show_members_command
)
from bot.handlers.error_handler import error_handler
from bot.handlers.report_handler import report_command, DESCRIPTION, description_handler, \
    send_without_description_handler, cancel_handler, cancel_keyboard_button, without_description_keyboard_button
from sql import get_tables, get_database_revision


bot = Bot(BOT_TOKEN)

# Registering logger here
app_logging.register_bot(bot)
logger = app_logging.get_logger(__name__)


def setup():
    """
    Setting up updater.
    Checking the connectivity with the database.

    Registered all handlers (for commands)

    Returns:
        dispatcher and updater
    """
    logger.info(f'Bot version: {BOT_VERSION}')
    logger.info(f"\n\tDB revision: {get_database_revision()}; \n\ttables: {get_tables()}")
    logger.info("Setting up bot...")
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
    dispatcher.add_handler(CommandHandler('show_members', show_members_command))

    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('about_me', about_me_command))

    # Registering conversation handlers here

    # Handler for the reports functionality
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('report', report_command)],
        states={
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.text(cancel_keyboard_button)
                                         & ~Filters.text(without_description_keyboard_button), description_handler),
                          MessageHandler(Filters.text(without_description_keyboard_button),
                                         send_without_description_handler)],
        },
        fallbacks=[MessageHandler(Filters.text(cancel_keyboard_button), cancel_handler)],
        per_user=True
    ))

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

    # Handle for errors
    dispatcher.add_error_handler(error_handler)

    _update_command_list()

    return dispatcher, updater


def _update_command_list():
    """Updates the bot command list at the startup of the bot."""

    commands_str = """
    create_queue - <queue name> Creates a new queue
    delete_queue - <queue name> Deletes the queue
    add_me - <queue name> Adds you to the queue
    remove_me - <queue name> Removes you from the queue
    skip_me - <queue name> Moves you down in the queue
    next - <queue name> Notifies next person in the queue and moves queue down
    show_queues - Shows all created queues
    show_members - <queue name> Resends queue message
    notify_all - Enables\\disables pinning the queues
    help - Shows description
    about_me - Detailed info about the bot
    report - [Description] report an error to the developer
    """
    command_name: str
    description: str
    commands_list = [BotCommand(command_name.strip(), description.strip()) for command_str
                     in commands_str.split('\n')
                     if command_str.strip()
                     for (command_name, description) in (command_str.split('-'),)]
    bot.set_my_commands(commands_list)
    logger.info('The commands list was updated.')


# noinspection PyUnusedLocal
def unexpected_message(update: Update, context: CallbackContext):
    logger.info(f"Unexpected message: [chat_id: {update.effective_chat.id}; message: {update.effective_message.text}]")
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
