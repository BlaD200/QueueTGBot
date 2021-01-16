"""This module contains the :class:`LoggingConfig` class."""

from logging import INFO, Formatter
from logging import Logger
from typing import Optional, List, NoReturn

from telegram import Bot

from app_logging.bot_cashing_handler import BotCashingHandler


class LoggingConfig:
    """The class contains all configuration variables and related methods."""

    def __init__(self) -> None:
        self._log_format = '%(asctime)s [%(levelname)-7s] %(name)s (%(funcName)s:%(lineno)d) | %(message)s'
        self._bot: Optional[Bot] = None
        self._log_buffer_size: int = 50
        self._bot_cashing_handler: Optional[BotCashingHandler] = None

        self._loggers: List[Logger] = []

    @property
    def log_format(self) -> str:
        """
        Returns: the log format for the logger.
        """
        return self._log_format

    @property
    def bot(self) -> Bot:
        """The bot instance, used in the :class:`BotCashingHandler` class."""
        return self._bot

    @bot.setter
    def bot(self, bot: Bot) -> NoReturn:
        self._bot = bot

    @property
    def bot_cashing_handler(self):
        """Returns the instance of the :class:`BotCashingHandler` class.
        """
        return self._bot_cashing_handler

    @property
    def loggers(self) -> List[Logger]:
        """
        Returns: the :obj:`list` of the Loggers, added in the ``add_logger`` method.
        """
        return self._loggers

    def add_logger(self, logger: Logger) -> NoReturn:
        """Adds the logger to the list of created loggers."""
        self._loggers.append(logger)

    def create_cashing_bot_handler(self) -> None:
        """
        Creates the :class:`BotCashingHandler` class, if it wasn't created before.

        Expected to be called after setting the bot.

        Raises:
            ValueError: If the bot is not set before calling.

        """
        if not self._bot:
            raise ValueError('The bot must be set before creating BotCashingHandler.')
        if not self._bot_cashing_handler:
            self._bot_cashing_handler = BotCashingHandler(self.bot, self._log_buffer_size)
            self._bot_cashing_handler.setLevel(INFO)
            self._bot_cashing_handler.setFormatter(Formatter(self._log_format))

    def update_loggers_with_cashing_bot_handler(self) -> None:
        """
        Adds :class:`BotCashingHandler` to the loggers' handlers
        to let the :class:`BotCashingHandler` store the last N log records and send them after request.

        Note:
            Loggers itself must be added in the ``add_logger`` method.

        Raises:
            AttributeError: If the bot or the BotCashingHandler was not set before calling
                and BotCashingHandler cannot be created.
        """
        if not self.bot or not self._bot_cashing_handler:
            raise AttributeError('Tried to register the CashingBotHandler '
                                 'before specified the handler itself or registered the bot.')
        if not self._bot_cashing_handler:
            self.create_cashing_bot_handler()

        for logger in self._loggers:
            if self._bot_cashing_handler not in logger.handlers:
                logger.addHandler(self._bot_cashing_handler)
