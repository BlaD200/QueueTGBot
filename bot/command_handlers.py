"""This module contains the functions that handle all commands supported by the bot."""

import logging

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from bot.chat_type_accepted import group_only_command
from localization.replies import (
    start_message_private, start_message_chat,
    unknown_command, unimplemented_command,
    create_queue_exist, create_queue_empty_name,
    help_message, help_message_in_chat,
    about_me_message,
    unexpected_error
)
from sql import create_session
from sql.domain import *


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def log_command(command_name: str = None):
    """
    Designed to be a decorator.
    Decorated function HAS TO have two arguments:
    :class:`telegram.Update` and :class:`telegram.CallbackContext`
    \n
    Logs a message with a command from a user with such information, as chat_type, chat_id, user_id and command args.

    Args:
        command_name: name of the command to be logged. If not passed will be logged the first word in received message.
    """

    def decorator_maker(f):
        def wrapped(update: Update, context: CallbackContext):
            chat_id = update.effective_chat.id
            chat_name = update.effective_chat.title
            user_id = update.effective_user.id
            chat_type = update.effective_chat.type
            args = ' '.join(context.args) if context.args is not None else update.effective_message.text
            info = f"chat_type: '{chat_type}', " \
                   f"chat_id: '{chat_id}', chat_name: '{chat_name}', user: '{user_id}', args: '{args}'"
            _command_name = command_name if command_name is not None else update.effective_message.text.split(' ')[0]
            if update.edited_message:
                logging.info(f"{_command_name}: [{info}] edited")
            else:
                logging.info(f"{_command_name} [{info}]")

            return f(update, context)

        return wrapped

    return decorator_maker


@log_command('start')
def start_command(update: Update, context: CallbackContext):
    """
    Handler for '/start' command.
    Sends ``bot.constants.start_message_private`` in private chats
    and ``bot.constants.start_message_chat`` in groups, public chats, ets.
    """
    chat_type = update.message.chat.type
    if chat_type == 'private':
        update.effective_message.reply_text(
            **start_message_private(fullname=update.message.from_user.full_name)
        )
    else:
        update.effective_message.reply_text(
            **start_message_chat(fullname=update.message.from_user.full_name,
                                 user_id=update.message.from_user.id)
        )


@log_command('create_queue')
@group_only_command
def create_queue_command(update: Update, context: CallbackContext):
    """Handler for '/create_queue <queue_name>' command"""
    # notify all members

    chat_id = update.effective_chat.id
    queue_name = ' '.join(context.args)
    if not queue_name:
        update.effective_chat.send_message(**create_queue_empty_name())
    else:
        session = create_session()
        count = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).count()
        if count == 1:
            update.effective_chat.send_message(
                **create_queue_exist(queue_name=queue_name)
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
                update.effective_chat.send_message(**unexpected_error())


@log_command('delete_queue')
@group_only_command
def delete_queue_command(update: Update, context: CallbackContext):
    """Handler for '/delete_queue <queue_name>' command"""
    ...


@log_command('show_queues')
@group_only_command
def show_queues_command(update: Update, context: CallbackContext):
    """Handler for '/show_queues' command"""
    ...


@log_command('help')
def help_command(update: Update, context: CallbackContext):
    """Handler for '/help' command"""
    if update.effective_chat.type == 'private':
        update.effective_message.reply_text(**help_message())
    else:
        update.effective_message.reply_text(**help_message_in_chat())


@log_command('about_me')
def about_me_command(update: Update, context: CallbackContext):
    """Handler for '/info' command"""
    update.effective_message.reply_text(**about_me_message())


@log_command('unsupported_command')
def unsupported_command_handler(update: Update, context: CallbackContext):
    """Handler for any command, which doesn't exist in the bot."""
    update.effective_message.reply_text(**unknown_command())


@log_command()
def unimplemented_command_handler(update: Update, context: CallbackContext):
    update.message.reply_text(**unimplemented_command())


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
