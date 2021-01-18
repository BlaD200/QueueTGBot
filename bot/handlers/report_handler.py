# Copyright (C) 2021 Vladyslav Synytsyn
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
from telegram.ext import CallbackContext, ConversationHandler

from app_logging import get_logger, BotCachingHandler
from app_logging.handler_logging import log_command
from localization.report_error_strings import (
    get_keyboard_for_report, report_error_message,
    thanks_for_feedback_message, cancel_report_message,
    thanks_for_feedback_without_description_message
)


logger = get_logger(__name__)
DESCRIPTION = 0

without_description_keyboard_button = get_keyboard_for_report()[0]
cancel_keyboard_button = get_keyboard_for_report()[1]


@log_command('report')
def report_command(update: Update, context: CallbackContext) -> int:
    """Handler for /report command.

    If the description was passed as the argument of the command, sends the report with it,
    otherwise, starts the conversation to ask the description.
    """
    if context.args:
        chat_id = update.effective_chat.id
        description = ' '.join(context.args)
        user_id = update.effective_user.id
        user_name = update.effective_user.full_name
        send_report(chat_id, description, user_id, user_name, update.effective_message)

        return ConversationHandler.END
    else:
        update.effective_message.reply_text(
            **report_error_message(),
            reply_markup=ReplyKeyboardMarkup(
                get_keyboard_for_report(),
                one_time_keyboard=True, resize_keyboard=True, selective=True),
        )

        return DESCRIPTION


def description_handler(update: Update, context: CallbackContext) -> int:
    """Handler for the message with description to the report.

    Triggered, if the user replied with the text, not from the keyboard, to the message
    sent in the ``report_command`` function.
    """
    chat_id = update.effective_chat.id
    description = update.effective_message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    send_report(chat_id, description, user_id, user_name, update.effective_message)

    return ConversationHandler.END


def send_without_description_handler(update: Update, context: CallbackContext) -> int:
    """Handler for the ``without_description_keyboard_button`` button."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    logger.info(f'Description was not specified by the user({update.effective_user.id}).',
                extra={**BotCachingHandler.get_logging_extra(chat_id, user_id, user_name)})
    update.effective_message.reply_text(**thanks_for_feedback_without_description_message(),
                                        reply_markup=ReplyKeyboardRemove(selective=True))

    return ConversationHandler.END


def cancel_handler(update: Update, context: CallbackContext) -> int:
    """Handler for the ``cancel_keyboard_button`` button."""
    logger.info(f'Report was cancelled by the user({update.effective_user.id})')
    update.effective_message.reply_text(**cancel_report_message(), reply_markup=ReplyKeyboardRemove(selective=True))

    return ConversationHandler.END


def send_report(chat_id: int, description: str, user_id: int, user_name: str, message: Message):
    """Logs the description and triggers the :class:`BotCachingHandler` to send the report to the admin."""
    logger.info(f'Description to the report: {description}'),
    logger.info(f'The user({user_id}) was sent the report with description',
                extra={**BotCachingHandler.get_logging_extra(chat_id, user_id, user_name, description)})
    message.reply_text(**thanks_for_feedback_message(),
                       reply_markup=ReplyKeyboardRemove(selective=True))
