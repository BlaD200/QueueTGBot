# Copyright (C) 2021 Vladyslav Synytsyn
from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger, BotCachingHandler


logger = get_logger(__name__)


def error_handler(update: Update, context: CallbackContext):
    logger.info(update)
    logger.info(f'context.bot_data: {context.bot_data}')
    logger.info(f'context.chat_data: {context.chat_data}')
    logger.info(f'context.user_data: {context.user_data}')
    chat_id = update.effective_chat.id
    logger.exception(f"Unexpected error: [chat_id: {chat_id}; error: {context.error}]",
                     extra={BotCachingHandler.flash_to_bot: True,
                            BotCachingHandler.error_from_chat_id: chat_id})


__all__ = [
    'error_handler'
]
