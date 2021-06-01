from telegram import Update, ReplyKeyboardRemove

from app_logging import get_logger
from localization.replies import remove_keyboard_message
from sql.domain import Chat


logger = get_logger(__name__)


def remove_user_keyboard(update: Update):
    """
    Sends message with :class:`telegram.ReplyKeyboardRemove` reply markup to remove the keyboard for the user.
    """
    message = update.effective_message.reply_text(
        **remove_keyboard_message(),
        reply_markup=ReplyKeyboardRemove(selective=True)
    )
    message.delete()
    logger.info("Keyboard was removed for user without reply.")


def send_message_if_not_silent_or_keyboard(chat: Chat, update: Update, alternate_condition=False, **kwargs):
    if (chat and not chat.silent_mode) or alternate_condition:
        update.effective_message.reply_text(**kwargs)
    else:
        logger.info(f"Sending reply to chat({chat.chat_id}) cancelled. Silent mode on.")
