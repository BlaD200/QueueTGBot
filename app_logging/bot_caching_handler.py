"""The module contains the ``BotCachingHandler`` class."""

import logging
from typing import List, Optional

from telegram import Bot

from bot.constants import ADMIN_ID


class BotCachingHandler(logging.StreamHandler):
    """
    The class registers to the :class:`logging.Logger` to cache and send logs directly to the bot's admin.

    This class should be added to the logger handlers by ``logger.addHandler(...)`` method.
    It stores the last N log records, the number of which specified in ``log_buffer_size`` and then
    when receiving ``flash_to_bot=True`` flag in the log.<level>() method,
    flushes all records to the chat with ADMIN_ID user (specified in the ``bot.constants.py`` file).

    The ``error_from_chat_id`` also should be specified, otherwise, the bot will send the message
    with the ``chat_id=UNSPECIFIED`` in it.

    The ``error_description`` could also be passed to this handler in the ``extra`` dictionary, and, if passed,
    the description also is sent in the message to the admin. It can be used, for example,
    if a known error occurred and the description can help to fix the error faster,
    or for error reporting from the users.

    Note:
        Use ``BotCachingHandler.flash_to_bot``, ``BotCachingHandler.error_from_chat_id``, and
        ``BotCachingHandler.error_description`` as the keys in the extra dictionary.
        Or, if nothing else should be passed in it, you can use the ``get_logging_extra`` method,
        pass parameters to it and then unpack the result dictionary by ****** operator.

    Examples:
        >>> from app_logging import get_logger, register_bot
        >>> from bot.constants import BOT_TOKEN
        >>> from telegram.bot import Bot
        >>>
        >>> logger = get_logger(__name__)
        >>> bot = Bot(BOT_TOKEN)
        >>> register_bot(bot)
        >>>
        >>> logger.info('Message to log',
        ...        extra={BotCachingHandler.flash_to_bot: True,
        ...               BotCachingHandler.error_from_chat_id: -1,
        ...               BotCachingHandler.error_description: 'Description'})

    See Also:
        https://docs.python.org/3/howto/logging-cookbook.html
    """

    flash_to_bot: str = 'flash_to_bot'
    """The key for the ``extra``, has to be set to **True** if the log message must be sent to the admin."""
    error_from_chat_id: str = 'error_from_chat_id'
    """The key for the ``extra``, has to be set to know in which chat the error has occurred."""
    error_description: str = 'error_description'
    """The key for the ``extra``, has to be set to send the **description** of the error."""

    def __init__(self, bot: Bot, log_buffer_size: int) -> None:
        """
        Args:
            bot: the ``Bot`` object, that will be used to send the error message to the admin.
            log_buffer_size: the number of logs, that will be cached and sent.
        """
        logging.StreamHandler.__init__(self)

        self.log_buffer: List[str] = []
        self.telegram_bot = bot
        self.log_buffer_size = log_buffer_size

    def emit(self, record: logging.LogRecord) -> None:
        """This methods is called, when the user called the ``logger.info()`` or higher level method."""
        try:
            msg = self.format(record)
            self.log_buffer.append(msg)
            if len(self.log_buffer) > self.log_buffer_size:
                self.log_buffer.pop(0)

            if record.__dict__.get('flash_to_bot', False):
                message_text: str
                error_from_chat_id = record.__dict__.get('error_from_chat_id', 'UNSPECIFIED')
                if record.__dict__.get('error_description', None):
                    error_description = record.__dict__.get('error_description')
                    message_text = f'An error was reported from the chat_id {error_from_chat_id} ' \
                                   f'with the following description: \n{error_description}\n\n'
                else:
                    message_text = f'An error was occurred in chat_id {error_from_chat_id}.\n'
                message_text += f'Sending last {self.log_buffer_size} log records: \n'
                message_text += ''.join([f'{log}\n' for log in self.log_buffer])

                self.telegram_bot.send_message(
                    chat_id=ADMIN_ID,
                    text=message_text
                )
        except Exception:
            self.handleError(record)

    @staticmethod
    def get_logging_extra(error_from_chat_id: int, error_description: Optional[str] = None):
        """
        Creates and returns the dictionary with info, that have to be passed to the ``extra`` dictionary.

        Could be unpacked with the ****** operator.

        Args:
            error_from_chat_id: the chat_id in which the error has occurred.
            error_description: the description of the error.
        Returns:
            the ``dict`` objects, that have to be passed to the ``log.<level>()`` method.
        """
        return {
            BotCachingHandler.flash_to_bot: True,
            BotCachingHandler.error_from_chat_id: error_from_chat_id,
            BotCachingHandler.error_description: error_description
        }


__all__ = [
    'BotCachingHandler'
]
