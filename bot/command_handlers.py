import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from bot.constants import start_message_private, unknown_command, unimplemented_command, help_message, about_me_message


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext):
    log_command(update, context, 'start')

    chat_type = update.message.chat.type
    if chat_type == 'private':
        update.effective_message.reply_text(
            text=start_message_private.format(fullname=update.message.from_user.full_name)
        )
    else:
        update.effective_message.reply_text(
            text=f"Hello, [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})!",
            parse_mode=ParseMode.MARKDOWN_V2
        )


def create_queue_command(update: Update, context: CallbackContext):
    """Handler for '/create_queue <queue_name>' command"""
    log_command(update, context, 'create_queue')
    # notify all members
    ...


def delete_queue_command(update: Update, context: CallbackContext):
    """Handler for '/delete_queue <queue_name>' command"""
    log_command(update, context, 'delete_queue')
    ...


def show_queues_command(update: Update, context: CallbackContext):
    """Handler for '/show_queues' command"""
    log_command(update, context, 'show_queues')
    ...


def help_command(update: Update, context: CallbackContext):
    """Hadler for '/help' command"""
    log_command(update, context, 'help')
    update.effective_message.reply_text(help_message)


def about_me_command(update: Update, context: CallbackContext):
    """Handler for '/info' command"""
    log_command(update, context, 'info')
    update.effective_message.reply_text(about_me_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def unsupported_command_handler(update: Update, context: CallbackContext):
    """Handler for any command, which doesn't exist in the bot."""
    log_command(update, context, 'unsupported command')
    update.effective_message.reply_text(unknown_command)


def unimplemented_command_handler(update: Update, context: CallbackContext):
    log_command(update, context, update.effective_message.text.split(' ')[0])
    update.message.reply_text(unimplemented_command)


def log_command(update: Update, context: CallbackContext, command_name: str):
    """
    Logs a message with a command from a user with such information, as chat_type, chat_id, user_id and command args.
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    args = ' '.join(context.args) if context.args is not None else update.effective_message.text
    info = f"chat_type: '{chat_type}', chat: '{chat_id}', user: '{user_id}', args: '{args}'"
    if update.edited_message:
        logging.info(f"{command_name}: [{info}] edited")
    else:
        logging.info(f"{command_name} [{info}]")
