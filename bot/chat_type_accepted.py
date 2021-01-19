# Copyright (C) 2021 Vladyslav Synytsyn
"""This module contains decorators, used to manage command accessibility from different chat types."""
from typing import Callable, Any

from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger
from localization.replies import private_unaccepted


logger = get_logger(__name__)


def group_only_command(handler: Callable[[Update, CallbackContext], Any]):
    """
    Decorator function. \n

    It is used to decorate command handlers, that HAVE TO accept two arguments:
    :class:`telegram.Update` and :class:`telegram.CallbackContext` \n

    The wrapped function will be called ONLY if the chat type is 'group' or 'supergroup'.
    Otherwise will be sent ``bot.constants.private_unaccepted``

    :param handler: handler function for command
    :return: given function wrapped with chat type check.
    """

    def group_only_command_wrapper(update: Update, context: CallbackContext):
        if update.effective_chat.type == 'private' or update.effective_chat.type == 'channel':
            update.effective_message.reply_text(**private_unaccepted())
        else:
            return handler(update, context)

    return group_only_command_wrapper


def private_only_handler(handler: Callable[[Update, CallbackContext], Any]):
    """
    Decorator function.

    The decorated function will be called ONLY if the chat type is 'private', otherwise, the call will be omitted.

    Note:
        It is used to decorate handlers, that HAVE TO accept two arguments:
        :class:`telegram.Update` and :class:`telegram.CallbackContext`

        You can also use ``Filters.chat_type.private`` for filtering your messages.

    Args:
        handler: handler function

    Returns:
        given function with the chat type check
    """

    def private_only_handler_wrapper(update: Update, context: CallbackContext):
        if update.effective_chat.type == 'private':
            return handler(update, context)

    return private_only_handler_wrapper


__all__ = [
    'group_only_command',
    'private_only_handler'
]
