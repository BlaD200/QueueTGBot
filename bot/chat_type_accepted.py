# Copyright (C) 2021 Vladyslav Synytsyn
"""This module contains decorators, used to manage command accessibility from different chat types."""
from typing import Callable, Any

from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger
from localization.info_and_help_strings import InfoAndHelpStrings
from sql import create_session
from sql.domain import Chat


logger = get_logger(__name__)


def group_only_handler(handler: Callable[[Update, CallbackContext], Any]):
    """
    Decorator function. \n

    It is used to decorate handlers, that HAVE TO accept two arguments:
    :class:`telegram.Update` and :class:`telegram.CallbackContext` \n

    Note:
        The wrapped function will be called ONLY if the chat type is 'group' or 'supergroup'.
        Otherwise will be sent ``bot.constants.private_unaccepted_message``

        You can also use ``Filters.chat_type.private`` for filtering your messages.

    Args:
        handler: handler function for command
    Returns:
        given function wrapped with chat type check.
    """

    def group_only_command_wrapper(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        session = create_session()
        chat: Chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()

        if chat:
            info_strings = InfoAndHelpStrings(chat.language)
        else:
            info_strings = InfoAndHelpStrings('en')
        if update.effective_chat.type == 'private' or update.effective_chat.type == 'channel':
            update.effective_message.reply_text(**info_strings.private_unaccepted_message())
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
    'group_only_handler',
    'private_only_handler'
]
