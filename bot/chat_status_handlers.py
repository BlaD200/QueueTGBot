"""This module contains the functions that handle joining and leaving from the chat."""

import logging

from sqlalchemy.exc import IntegrityError
from telegram import Update, User
from telegram.ext import CallbackContext

from sql import create_session
from sql.domain import *


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def new_chat_member_handler(update: Update, context: CallbackContext):
    """
    Triggered when someone joined the group.
    Also triggered, when this bot is added to the group and, in that case, saving the chat id and name to DB.

    Args:
        update: :class:`telegram.Update`
        context: :class:`telegram.CallbackContext`
    """
    member: User
    is_me = [member for member in update.effective_message.new_chat_members if member.id == context.bot.id]
    logger.info(f"new member: "
                f"\n\tis_me: {len(is_me) == 1}"
                f"\n\t[chat_id: {update.effective_chat.id}; "
                f"\n\tnew_chat_members: {[str(i) for i in update.effective_message.new_chat_members]}; "
                f"\n\tfrom: {update.effective_message.from_user}]")

    chat = Chat(chat_id=update.effective_chat.id, name=update.effective_chat.title)
    logger.info(f"Joined to chat_id ({update.effective_chat.id})")

    session = create_session()
    try:
        session.add(chat)
        session.commit()
        logger.info(f"Chat saved to DB ({chat.chat_id})")
    except IntegrityError as e:
        logger.error("ERROR while adding to DB:\n" + str(e))
        session.rollback()
        logger.warning("Session was rolled back.")


def left_chat_member_handler(update: Update, context: CallbackContext):
    """
    Triggered when someone left the group.
    Also triggered, when this bot is removed from the group and, in that case,
    deleting the chat and all related info from DB.

    Args:
        update: :class:`telegram.Update`
        context: :class:`telegram.CallbackContext`
    """
    is_me = update.effective_message.left_chat_member.id == context.bot.id
    chat_id = update.effective_chat.id
    logger.info(f"left member: "
                f"\n\tis_me: {is_me}"
                f"\n\t[chat_id: {chat_id}; "
                f"\n\tleft_chat_member: {update.effective_message.left_chat_member}; "
                f"\n\tfrom: {update.effective_message.from_user}]")

    logger.info(f"Removed from chat_id {chat_id}")

    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat is None:
        logger.warning("Expected the chat(id='') was in DB, but it wasn't found.")
        session.rollback()
        logger.warning("Session was rolled back.")
        return
    else:
        session.delete(chat)
        session.commit()
        logger.info(f"Chat removed from DB ({chat.chat_id})")


__all__ = [
    'new_chat_member_handler',
    'left_chat_member_handler'
]
