# Copyright (C) 2021 Vladyslav Synytsyn
"""This module encapsulates all things related to logging in this app."""

import logging

from telegram import Bot

from app_logging.bot_caching_handler import BotCachingHandler
from app_logging.logging_config import LoggingConfig


__log_config: LoggingConfig = LoggingConfig()


def get_logger(name: str) -> logging.Logger:
    """
    The function creates, setups and return the instance of the :class:`logging.Logger`.

    Uses the :class:`LoggingConfig` to configure the logger.

    :param name: the name of the module, that will be used in the log messages
    :return: the instance of configured logger
    """
    logger = logging.Logger(name)
    logger.setLevel(logging.INFO)

    logger.addHandler(__get_stream_handler())
    # if __log_config.bot:
    #     logger.addHandler(__log_config.bot_cashing_handler)

    # __log_config.add_logger(logger)

    return logger


def register_bot(bot: Bot, bot_log_buffer_size: int = 50) -> None:
    """
    Used to register the bot to the :class:`BotCachingHandler`.

    The bot has to be registered in case you want to receive the error messages
    directly to your telegram chat with this bot.

    See also:
        :class:`BotCachingHandler` for more information

    Args:
        bot: the instance of the bot, to be registered
        bot_log_buffer_size: the number of the messages, :class:`BotCachingHandler` will keep
    """
    __log_config.bot = bot
    __log_config.log_buffer_size = bot_log_buffer_size
    __log_config.create_cashing_bot_handler()

    __log_config.update_loggers_with_cashing_bot_handler()


def __get_stream_handler() -> logging.StreamHandler:
    """
    Configures :class:`logging.StreamHandler` and returns it.

    :return: configured StreamHandler
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(__log_config.log_format))
    # stream_handler.setStream(sys.stdout)
    return stream_handler


def __get_cashing_bot_handler():
    """
    Configures :class:`BotCachingHandler` and returns it.

    Note:
        The instance of the :class:`BotCachingHandler` is created only once and then reused.

    Returns:
         configured BotCachingHandler
    """
    if not __log_config.bot_cashing_handler:
        __log_config.create_cashing_bot_handler()

    return __log_config.bot_cashing_handler


__all__ = [
    'get_logger',
    'register_bot',
    'BotCachingHandler'
]
