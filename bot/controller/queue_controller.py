import logging

from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.error import BadRequest

from app_logging import get_logger
from bot.callbacks.callback_buttons import get_member_action_buttons
from bot.utils import remove_user_keyboard, send_message_if_not_silent_or_keyboard
from localization.replies import (
    create_queue_exist, queue_not_exist, deleted_queue_message, show_queue_members, no_rights_to_unpin_message,
    create_queue_unsupported_name
)
from sql import create_session
from sql.domain import Queue, Chat


logger: logging.Logger = get_logger(__name__)


def create_queue_action(update: Update, queue_name: str, bot):
    chat_id = update.effective_chat.id

    session = create_session()
    count = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).count()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if count == 1:
        logger.info("Creating a queue with an existing name")
        send_message_if_not_silent_or_keyboard(
            chat, update,
            'create_queue' not in update.effective_message.text,
            **create_queue_exist(queue_name=queue_name), reply_markup=ReplyKeyboardRemove(selective=True)
        )
    else:
        queue = Queue(name=queue_name, chat_id=chat_id)
        message = None
        try:
            session.add(queue)
            session.commit()

            chat: Chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()

            message = update.effective_chat.send_message(
                **show_queue_members(queue.name),
                **get_member_action_buttons(queue.queue_id, not chat.notify)
            )

            queue.message_id_to_edit = message.message_id
            session.merge(queue)
            session.commit()

            logger.info(f"New queue created: \n\t{queue}")

            # Send the reply to hide the keyboard for the user if one was present
            if 'create_queue' not in update.effective_message.text:
                remove_user_keyboard(update)

            # Checking if the bot has rights to pin the message.
            if bot.get_chat_member(chat_id, bot.id).can_pin_messages:
                if queue.chat.notify:
                    message.pin()
            # If the message should be pinned, but the bot hasn't got rights.
            elif queue.chat.notify:
                send_message_if_not_silent_or_keyboard(
                    chat, update,
                    **create_queue_exist(queue_name=queue_name), reply_markup=ReplyKeyboardRemove(selective=True)
                )
        except Exception as e:
            logger.exception(f"ERROR when creating queue: \n\t{queue} "
                             f"with message: \n{e}")
            update.effective_chat.send_message(**create_queue_unsupported_name())
            session.delete(queue)
            session.commit()
            logger.warning("Queue was deleted")
            if message:
                message.delete()


def delete_queue_action(update: Update, queue_name: str, bot):
    chat_id = update.effective_chat.id

    session = create_session()
    queue: Queue = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).first()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if queue is None:
        logger.info("Deletion nonexistent queue.")
        send_message_if_not_silent_or_keyboard(
            chat, update,
            'delete_queue' not in update.effective_message.text,
            **queue_not_exist(queue_name=queue_name), reply_markup=ReplyKeyboardRemove(selective=True)
        )
    else:
        session.delete(queue)
        session.commit()
        logger.info(f"Deleted queue: \n\t{queue}")
        send_message_if_not_silent_or_keyboard(
            chat, update,
            'delete_queue' not in update.effective_message.text,
            **deleted_queue_message(), reply_markup=ReplyKeyboardRemove(selective=True)
        )

        if bot.get_chat_member(chat_id, bot.id).can_pin_messages:
            try:
                bot.unpin_chat_message(chat_id, message_id=queue.message_id_to_edit)
            except BadRequest as e:
                logger.warning(f"ERROR when tried to unpin "
                               f"message({queue.message_id_to_edit}) in queue({queue.queue_id}):\n\t"
                               f"{e}")
            try:
                bot.edit_message_text(
                    **show_queue_members(queue_name),
                    chat_id=chat_id,
                    message_id=queue.message_id_to_edit,
                    reply_markup=InlineKeyboardMarkup([]))
            except BadRequest as e:
                logger.warning(f"ERROR when tried to remove callback buttons for "
                               f"the message({queue.message_id_to_edit}) in the queue({queue.queue_id}):\n\t"
                               f"{e}")
        else:
            send_message_if_not_silent_or_keyboard(
                chat, update,
                **no_rights_to_unpin_message()
            )
