from typing import List

from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from telegram import Update, Bot
from telegram.error import BadRequest

from app_logging import get_logger
from bot.callbacks.callback_buttons import get_member_action_buttons
from bot.constants import CACHE_TIME
from localization.replies import already_in_the_queue, show_queue_members, not_in_the_queue_yet, next_reached_queue_end, \
    next_member_notify, cannot_skip
from sql import create_session
from sql.domain import QueueMember, Queue


logger = get_logger(__name__)


def add_me_action(update: Update, queue: Queue, bot: Bot):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    queue_id = queue.queue_id

    session = create_session()
    member = (session
              .query(QueueMember)
              .filter(QueueMember.queue_id == queue_id,
                      QueueMember.user_id == user_id).first())
    if member is not None:
        logger.info("Already in the queue.")
        if update.callback_query:
            update.callback_query.answer(**already_in_the_queue(), cache_time=CACHE_TIME)
        else:
            # TODO add silence setting
            update.effective_message.reply_text(**already_in_the_queue())
        return

    last_member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue_id)
            .order_by(QueueMember.user_order.desc())
            .first()
    )
    if last_member is None:
        user_order = 1
    else:
        user_order = last_member.user_order + 1
    member = QueueMember(user_id=user_id, fullname=update.effective_user.full_name,
                         user_order=user_order, queue_id=queue_id)
    session.add(member)
    session.commit()
    logger.info(f"Added member to queue: \n\t{member}")

    __edit_queue_members_message(queue, chat_id, bot)
    if update.callback_query:
        update.callback_query.answer()


def remove_me_action(update: Update, queue: Queue, bot: Bot):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    session = create_session()
    member: QueueMember = (session
                           .query(QueueMember)
                           .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_id == user_id)
                           .first())
    if member is None:
        logger.info('Not yet in the queue')
        if update.callback_query:
            update.callback_query.answer(**not_in_the_queue_yet(), cache_time=CACHE_TIME)
        else:
            # TODO add silence setting
            update.effective_message.reply_text(**not_in_the_queue_yet())
    else:
        # If it was the last member return turn to the previous one
        last_member: QueueMember = (
            session
                .query(QueueMember)
                .filter(QueueMember.queue_id == queue.queue_id)
                .order_by(QueueMember.user_order.desc())
                .first()
        )
        if queue.current_order == last_member.user_order:
            queue.current_order = queue.current_order - 1
            session.merge(queue)
            logger.info(f'Updated current_order in queue: \n\t{queue}')

        session.delete(member)
        # Updating user_order in queue_members table
        # to move down all users with user_order greater than the value of deleted user
        update_stmt: TextClause = text('UPDATE queue_member '
                                       'SET user_order = user_order - 1 '
                                       'WHERE user_order > :deleted_user_order;')
        session.execute(update_stmt, {'deleted_user_order': member.user_order})

        session.commit()

        logger.info(f'User removed from queue (queue_id={queue.queue_id})')
        logger.info(f'Updated user_order in queue({queue.queue_id}) for users(order>{member.user_order})')

        __edit_queue_members_message(queue, chat_id, bot)
        if update.callback_query:
            update.callback_query.answer()


def skip_me_action(update: Update, queue: Queue, bot: Bot):
    chat_id = update.effective_chat.id
    reply_markup = update.effective_message.reply_markup
    session = create_session()

    member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue.queue_id,
                    QueueMember.user_id == update.effective_user.id)
            .first())
    if member is None:
        logger.info('Not yet in the queue')
        if update.callback_query:
            update.callback_query.answer(**not_in_the_queue_yet(), cache_time=CACHE_TIME)
        else:
            # TODO add silence setting
            update.effective_message.reply_text(**not_in_the_queue_yet())
    else:
        next_member: QueueMember = (
            session
                .query(QueueMember)
                .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_order == member.user_order + 1)
                .first()
        )
        if next_member is not None:
            member.user_order = member.user_order + 1
            next_member.user_order = next_member.user_order - 1
            session.add_all([member, next_member])
            session.commit()
            logger.info(f'Skip queue_member({member.user_id}) in the queue({queue.queue_id})')

            __edit_queue_members_message(queue, chat_id, bot)
            if update.callback_query:
                update.callback_query.answer()
        else:
            logger.info(f'Cancel skipping because of no other members in queue({queue.queue_id})')
            if update.callback_query:
                update.callback_query.answer(**cannot_skip(), cache_time=CACHE_TIME)
            else:
                # TODO add silence setting
                update.effective_message.reply_text(**cannot_skip())


def next_action(update: Update, queue: Queue, bot: Bot):
    order = queue.current_order + 1
    queue.current_order = order
    reply_markup = update.effective_message.reply_markup

    session = create_session()
    member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_order == queue.current_order)
            .first()
    )
    if member is None:
        logger.info(f"Reached the end of the queue({queue.queue_id})")
        if update.callback_query:
            update.callback_query.answer(**next_reached_queue_end(), cache_time=CACHE_TIME)
        else:
            # TODO add silence setting
            update.effective_message.reply_text(**next_reached_queue_end())
    else:
        logger.info(f'Next member: {member}')
        update.effective_chat.send_message(**next_member_notify(member.fullname, member.user_id, queue.name))

        session.merge(queue)
        session.commit()
        logger.info(f'Updated current_order: \n\t{queue}')

        __edit_queue_members_message(queue, update.effective_chat.id, bot)
    if update.callback_query:
        update.callback_query.answer()


def show_queue_members_action(chat_id: int, queue: Queue, bot):
    member_names = __get_queue_members(queue)
    message = bot.send_message(
        chat_id=chat_id,
        **show_queue_members(queue.name, member_names),
        **get_member_action_buttons(queue.queue_id)
    )
    if message:
        try:
            bot.delete_message(chat_id=chat_id, message_id=queue.message_id_to_edit)
        except BadRequest as e:
            logger.exception(f'Error when deleting the previously sent message: {e}')
        queue.message_id_to_edit = message.message_id

        session = create_session()
        session.add(queue)
        session.commit()

        logger.info(f'Updated message_to_edit_id in queue:\n\t{queue}')


def __edit_queue_members_message(queue: Queue, chat_id: int, bot):
    member_names = __get_queue_members(queue)

    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=queue.message_id_to_edit,
            **get_member_action_buttons(queue.queue_id),
            **show_queue_members(queue.name, member_names, queue.current_order)
        )
    except BadRequest as e:
        logger.exception(f'ERROR when editing the message({queue.message_id_to_edit}) for queue({queue.queue_id}): \n\t'
                         f'{e}')
        logger.warning(f'Sending a new message for the queue({queue.queue_id}) because of the previous error.')

        show_queue_members_action(chat_id, queue, bot)
    logger.info(f'Edited message: chat_id={chat_id}, message_id={queue.message_id_to_edit}')


def __get_queue_members(queue: Queue) -> List[str]:
    session = create_session()
    members = (session
               .query(QueueMember)
               .filter(QueueMember.queue_id == queue.queue_id)
               .order_by(QueueMember.user_order)
               .all()
               )
    member_names = [member.fullname for member in members]
    return member_names



