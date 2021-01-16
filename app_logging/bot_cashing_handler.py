import logging
from typing import List, Optional

from telegram import Bot

from bot.constants import ADMIN_ID


class BotCashingHandler(logging.StreamHandler):
    flash_to_bot: str = 'flash_to_bot'
    error_from_chat_id: str = 'error_from_chat_id'
    error_description: str = 'error_description'

    def __init__(self, bot: Bot, log_buffer_size: int) -> None:
        logging.StreamHandler.__init__(self)

        self.log_buffer: List[str] = []
        self.telegram_bot = bot
        self.log_buffer_size = log_buffer_size

    def emit(self, record: logging.LogRecord) -> None:
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
        return {
            BotCashingHandler.flash_to_bot: True,
            BotCashingHandler.error_from_chat_id: error_from_chat_id,
            BotCashingHandler.error_description: error_description
        }


__all__ = [
    'BotCashingHandler'
]
