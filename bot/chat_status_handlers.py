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


def __save_chat_to_db(chat_id: int, chat_title: str):
    """
    Saves chat to DB with given ``chat_id`` and ``chat_title``.

    Args:
        chat_id: id of the chat that was created
        chat_title: name of the chat that was created
    """
    chat = Chat(chat_id=chat_id, name=chat_title)

    session = create_session()
    try:
        session.add(chat)
        session.commit()
        logger.info(f"Chat saved to DB ({chat.chat_id})")
    except IntegrityError as e:
        logger.error("ERROR while adding to DB:\n" + str(e) + '\n')
        session.rollback()
        logger.warning("Session was rolled back.")


# noinspection PyUnusedLocal
def new_group_created_handler(update: Update, context: CallbackContext):
    """
    Triggered when a new group is created with this bot in it
    and save the chat id and name to DB.

    Args:
        update: :class:`telegram.Update`
        context: :class:`telegram.CallbackContext`
    """
    chat_id = update.effective_chat.id
    logger.info(f'Chat with id({chat_id}) was created.')

    __save_chat_to_db(chat_id, update.effective_chat.title)


def new_group_member_handler(update: Update, context: CallbackContext):
    """
    Triggered when someone joined the group.
    Also triggered, when this bot is added to the group and, in that case, saving the chat id and name to DB.

    Args:
        update: :class:`telegram.Update`
        context: :class:`telegram.CallbackContext`
    """
    member: User
    is_me = [member for member in update.effective_message.new_chat_members if member.id == context.bot.id]
    chat_id = update.effective_chat.id
    logger.info(f"new member: "
                f"\n\tis_me: {len(is_me) == 1}"
                f"\n\t[chat_id: {chat_id}; "
                f"\n\tnew_chat_members: {[str(i) for i in update.effective_message.new_chat_members]}; "
                f"\n\tfrom: {update.effective_message.from_user}]")

    if is_me:
        logger.info(f'Joined to chat with id({chat_id}).')
        __save_chat_to_db(chat_id, update.effective_chat.title)


def left_group_member_handler(update: Update, context: CallbackContext):
    """
    Triggered when someone left the group.
    Also triggered, when this bot is removed from the group and, in that case,
    deleting the chat and all related info from DB.

    Note:
        If someone has left the group and the bot remained in it alone,
        the bot will leave the group too.

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
                f"\n\tfrom: {update.effective_message.from_user}"
                f"\n\tmembers left: {update.effective_chat.get_members_count()}]")

    if is_me or update.effective_chat.get_members_count() == 1:
        if update.effective_chat.get_members_count() == 1:
            update.effective_chat.get_members_count()
            logger.info(f'The bot has left from the chat({chat_id}) because only it left in the group.')
        else:
            logger.info(f"Removed from chat_id {chat_id}")

        session = create_session()
        chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
        if chat is None:
            logger.warning(f"Expected the chat(id={chat_id}) was in DB, but it wasn't found.")
            return
        else:
            session.delete(chat)
            session.commit()
            logger.info(f"Chat removed from DB ({chat.chat_id})")


# noinspection PyUnusedLocal
def group_migrated_handler(update: Update, context: CallbackContext):
    """
    Triggers when the group migrated from the normal group to supergroup
    and updates the group id in the DB.

    Note:
        This method triggers twice:

        * first time ``update.effective_chat.id`` contains id assigned to normal group
            and ``update.effective_message.migrate_to_chat_id`` contains id that chat will migrate to.

        * second time ``update.effective_chat.id`` contains id assigned to supergroup
            and ``update.effective_message.migrate_from_chat_id`` contains an id
            that was assigned to the group before migration.

    Args:
        update: :class:`telegram.Update`
        context: :class:`telegram.CallbackContext`
    """
    if update.effective_message.migrate_to_chat_id:
        logger.info(f'Migrated to '
                    f'supergroup(id={update.effective_message.migrate_to_chat_id}) '
                    f'from group(id={update.effective_chat.id}).')
    else:
        logger.info(f'Migrated '
                    f'from group(id={update.effective_message.migrate_from_chat_id}) '
                    f'to supergroup(id={update.effective_chat.id})')

        session = create_session()
        chat = session.query(Chat).filter(Chat.chat_id == update.effective_message.migrate_from_chat_id).first()
        if chat is None:
            __save_chat_to_db(update.effective_chat.id, update.effective_chat.title)
        else:
            chat.chat_id = update.effective_chat.id
            session.commit()
            logger.info(f'Updated chat_id for chat({update.effective_chat.id})')


__all__ = [
    'new_group_created_handler',
    'new_group_member_handler',
    'left_group_member_handler',
    'group_migrated_handler'
]
