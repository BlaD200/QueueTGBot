"""This module contains decorators, used to manage command accessibility from different chat types."""

from telegram import Update
from telegram.ext import CallbackContext

from localization.replies import private_unaccepted


def group_only_command(fn):
    """
    Decorator function. \n

    It is used to decorate command handlers, that HAVE TO accept two arguments:
    :class:`telegram.Update` and :class:`telegram.CallbackContext` \n

    The wrapped function will be called ONLY if the chat type is 'group' or 'supergroup'.
    Otherwise will be sent ``bot.constants.private_unaccepted``

    :param fn: handler function for command
    :return: given function wrapped with chat type check.
    """

    def wrapper(update: Update, context: CallbackContext):
        if update.effective_chat.type == 'private' or update.effective_chat.type == 'channel':
            update.effective_message.reply_text(**private_unaccepted())
        else:
            return fn(update, context)

    return wrapper


__all__ = [
    'group_only_command'
]
