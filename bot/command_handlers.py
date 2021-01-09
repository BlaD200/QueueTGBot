"""This module contains the functions that handle all commands supported by the bot."""

import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from bot.constants import (
    start_message_private, start_message_chat,
    unknown_command, unimplemented_command,
    create_queue_exist, create_queue_empty_name,
    help_message, help_message_in_chat,
    about_me_message
)
# Registering logger here
from sql import create_session
from sql.domain import *


logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext):
    """
    Handler for '/start' command.
    Sends :const:`bot.constants.start_message_private` in private chats
    and :const:`bot.constants.start_message_chat` in groups, public chats, ets.
    """
    log_command(update, context, 'start')

    chat_type = update.message.chat.type
    if chat_type == 'private':
        update.effective_message.reply_text(
            text=start_message_private.format(fullname=update.message.from_user.full_name)
        )
    else:
        update.effective_message.reply_text(
            text=start_message_chat.format(fullname=update.message.from_user.full_name,
                                           user_id=update.message.from_user.id),
            parse_mode=ParseMode.MARKDOWN_V2
        )


def create_queue_command(update: Update, context: CallbackContext):
    """Handler for '/create_queue <queue_name>' command"""
    log_command(update, context, 'create_queue')
    # notify all members
    chat_id = update.effective_chat.id

    queue_name = ' '.join(context.args)
    if not queue_name:
        update.effective_chat.send_message(
            text=create_queue_empty_name,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        session = create_session()
        count = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).count()
        if count == 1:
            update.effective_chat.send_message(
                text=create_queue_exist.format(queue_name=queue_name),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            queue = Queue(name=queue_name, notify=True, chat_id=chat_id)
            try:
                session.add(queue)
                session.commit()
                logger.info(f"New queue created: \n\t{queue}")

                update.effective_chat.send_message(
                    text=f"*{queue_name}*\n\n"
                         "Members:\n",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"ERROR when creating queue: \n\t{queue}"
                             f"with message: \n{e}")
                update.effective_chat.send_message("Something went wrong...😢😢")


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
    if update.effective_chat.type == 'private':
        update.effective_message.reply_text(help_message)
    else:
        update.effective_message.reply_text(help_message_in_chat)


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
    chat_name = update.effective_chat.title
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    args = ' '.join(context.args) if context.args is not None else update.effective_message.text
    info = f"chat_type: '{chat_type}', " \
           f"chat_id: '{chat_id}', chat_name: '{chat_name}', user: '{user_id}', args: '{args}'"
    if update.edited_message:
        logging.info(f"{command_name}: [{info}] edited")
    else:
        logging.info(f"{command_name} [{info}]")


__all__ = [
    'start_command',
    'create_queue_command',
    'delete_queue_command',
    'show_queues_command',
    'help_command',
    'about_me_command',
    'unsupported_command_handler',
    'unimplemented_command_handler'

]
