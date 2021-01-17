"""This module contains the decorator functions, that can be used for logging handler calls."""
from typing import Callable, Any

from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger


logger = get_logger(__name__)


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

    def log_command_decorator_maker(command_handler: Callable[[Update, CallbackContext], Any]):
        def log_command_wrapped(update: Update, context: CallbackContext):
            chat_id = update.effective_chat.id
            chat_name = update.effective_chat.title
            user_id = update.effective_user.id
            chat_type = update.effective_chat.type
            args = ' '.join(context.args) if context.args is not None else update.effective_message.text
            info = f"chat_type: '{chat_type}', " \
                   f"chat_id: '{chat_id}', chat_name: '{chat_name}', user: '{user_id}', args: '{args}'"
            _command_name = command_name if command_name is not None else update.effective_message.text.split(' ')[0]
            if update.edited_message:
                logger.info(f"{_command_name}: [{info}] edited")
            else:
                logger.info(f"{_command_name} [{info}]")

            return command_handler(update, context)

        return log_command_wrapped

    return log_command_decorator_maker


__all__ = [
    'log_command'
]
