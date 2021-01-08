import logging

from telegram import Bot, User, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from bot.command_handlers import (
    start_command,
    create_queue_command,
    delete_queue_command,
    show_queues_command,
    help_command,
    about_me_command,
    unimplemented_command_handler,
    unsupported_command_handler
)
from bot.config import BOT_TOKEN
from sql import create_session, get_tables, get_database_revision


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)


def setup():
    """
    Setting up updater.
    Creating connection to the database.

    Registered all handlers (for commands)

    Returns:
        dispatcher and updater
    """
    session = create_session()
    logger.info(f"\n\tDB revision: {get_database_revision()}; \n\ttables: {get_tables()}")

    logging.info("Setting up bot...")
    # is_logged_out = bot.log_out()
    # logger.info(f"Logged out: {is_logged_out}")
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
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member_handler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unsupported_command_handler))
    dispatcher.add_handler(MessageHandler(Filters.all, unexpected_message))

    return dispatcher, updater


def new_chat_member_handler(update: Update, context: CallbackContext):
    member: User
    is_me = [member for member in update.effective_message.new_chat_members if member.id == context.bot.id]
    logger.info(f"new member: "
                f"\n\tis_me: {len(is_me) == 1}"
                f"\n\t[chat_id: {update.effective_chat.id}; "
                f"\n\tnew_chat_members: {[str(i) for i in update.effective_message.new_chat_members]}; "
                f"\n\tfrom: {update.effective_message.from_user}]")
    pass


def left_chat_member_handler(update: Update, context: CallbackContext):
    is_me = update.effective_message.left_chat_member.id == context.bot.id
    logger.info(f"left member: "
                f"\n\tis_me: {is_me}"
                f"\n\t[chat_id: {update.effective_chat.id}; "
                f"\n\tleft_chat_member: {update.effective_message.left_chat_member}; "
                f"\n\tfrom: {update.effective_message.from_user}]")
    pass


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


if __name__ == '__main__':
    test_server()
