"""This module contains the functions that handle all commands supported by the bot."""

import logging
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import TextClause
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.chat_type_accepted import group_only_command
from localization.replies import (
    start_message_private, start_message_chat,
    unknown_command, unimplemented_command,
    create_queue_exist, create_queue_empty_name,
    help_message, help_message_in_chat,
    about_me_message,
    unexpected_error, delete_queue_empty_name, queue_not_exist, deleted_queue_message, show_queues_message_empty,
    show_queues_message, command_empty_queue_name, show_queue_members, already_in_the_queue, no_rights_to_pin_message,
    not_in_the_queue_yet, cannot_skip, next_reached_queue_end, next_member_notify, reply_to_wrong_message_message,
    no_rights_to_unpin_message, notify_all_disabled_message, notify_all_enabled_message
)
from sql import create_session
from sql.domain import *


# Registering logger here
logger: logging.Logger = logging.getLogger(__name__)


def log_command(command_name: str = None):
    """
    Designed to be a decorator.
    Decorated function HAS TO have two arguments:
    :class:`telegram.Update` and :class:`telegram.CallbackContext`
    \n
    Logs a message with a command from a user with such information, as chat_type, chat_id, user_id and command args.

    Args:
        command_name: name of the command to be logged. If not passed will be logged the first word in received message.
    """

    def decorator_maker(f):
        def wrapped(update: Update, context: CallbackContext):
            chat_id = update.effective_chat.id
            chat_name = update.effective_chat.title
            user_id = update.effective_user.id
            chat_type = update.effective_chat.type
            args = ' '.join(context.args) if context.args is not None else update.effective_message.text
            info = f"chat_type: '{chat_type}', " \
                   f"chat_id: '{chat_id}', chat_name: '{chat_name}', user: '{user_id}', args: '{args}'"
            _command_name = command_name if command_name is not None else update.effective_message.text.split(' ')[0]
            if update.edited_message:
                logger.info(f"{_command_name}: [{info}] edited")
            else:
                logger.info(f"{_command_name} [{info}]")

            return f(update, context)

        return wrapped

    return decorator_maker


def __insert_queue_from_context(on_no_queue_log: str, on_not_exist_log: str, on_no_queue_reply: dict):
    """
    Decorator function.

    Tries to get the queue based on the replied message, if any,
    or using the name specified in the command args.

    * If the user replied to the message not generated for the queue
    (stored as ``message_id_to_edit`` in the :class:`Queue` class),
    the bot will reply with ``reply_to_wrong_message_message``.

    * If the user specified nonexistent name in command args,
    the bot will reply with ``queue_not_exist``

    * If the user didn't reply to the message, generated for the queue,
    and didn't specify the queue name in the command arguments,
    the bot will reply with ``on_no_queue_reply``

    Otherwise, the decorated function will be called with
    (:class:`telegram.Update`, :class:`telegram.CallbackContext`, :class:`Queue`) parameters.

    :param on_no_queue_log: given message will be logged, if the <b>third</b> condition is met
    :param on_not_exist_log: given message will be logged, if the <b>second</b> condition is met
    :param on_no_queue_reply: if the third condition is met, the bot will reply with this message.
    Have to be in the format, used in ``replies`` module.

    See Also:
        bot.localization.replies
    """

    def decorator_maker(command_handler_function):
        def wrapper(update: Update, context: CallbackContext):
            chat_id = update.effective_chat.id
            queue: Optional[Queue] = None

            session = create_session()
            # Trying to get the queue from message_id, that user replied to.
            if update.effective_message.reply_to_message:
                replied_message_id = update.effective_message.reply_to_message.message_id
                queue = (session
                         .query(Queue)
                         .filter(Queue.chat_id == chat_id, Queue.message_id_to_edit == replied_message_id)
                         .options(joinedload(Queue.members))
                         .first())
                # User replied to the wrong message (not with members) or to deleted queue.
                if not queue:
                    logger.info('Replied to wrong message or to the deleted queue.')
                    update.effective_message.reply_text(**reply_to_wrong_message_message())

            # User didn't reply to the message or replied to the wrong message.
            # Checks if there name specified in command arguments.
            queue_name = ' '.join(context.args)
            if context.args and not queue:
                queue = (session
                         .query(Queue)
                         .filter(Queue.chat_id == chat_id, Queue.name == queue_name)
                         .options(joinedload(Queue.members))
                         .first())
            if queue:
                return command_handler_function(update, context, queue)
            # The name was specified but queue with this name wasn't found in DB
            elif not queue and context.args:
                logger.info(on_not_exist_log)
                update.effective_message.reply_text(**queue_not_exist(queue_name=queue_name))
            else:
                logger.info(on_no_queue_log)
                update.effective_message.reply_text(**on_no_queue_reply)

        return wrapper

    return decorator_maker


@log_command('start')
def start_command(update: Update, context: CallbackContext):
    """
    Handler for '/start' command.
    Sends ``bot.constants.start_message_private`` in private chats
    and ``bot.constants.start_message_chat`` in groups, public chats, ets.
    """
    chat_type = update.message.chat.type
    if chat_type == 'private':
        logger.info(f'Started private chat with user:\n\t{update.effective_user}')
        update.effective_message.reply_text(
            **start_message_private(fullname=update.message.from_user.full_name)
        )
    else:
        logging.info(f'Start command in group: \n\t{update.effective_chat}')
        update.effective_message.reply_text(
            **start_message_chat(fullname=update.message.from_user.full_name,
                                 user_id=update.message.from_user.id)
        )


@log_command('create_queue')
@group_only_command
def create_queue_command(update: Update, context: CallbackContext):
    """Handler for '/create_queue <queue_name>' command"""

    chat_id = update.effective_chat.id
    queue_name = ' '.join(context.args)
    if not queue_name:
        logger.info("Creation a queue with empty name.")
        update.effective_chat.send_message(**create_queue_empty_name())
    else:
        session = create_session()
        count = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).count()
        if count == 1:
            logger.info("Creating a queue with an existing name")
            update.effective_chat.send_message(
                **create_queue_exist(queue_name=queue_name)
            )
        else:
            queue = Queue(name=queue_name, chat_id=chat_id)
            message = update.effective_chat.send_message(**show_queue_members(queue_name))
            try:
                queue.message_id_to_edit = message.message_id

                session.add(queue)
                session.commit()
                logger.info(f"New queue created: \n\t{queue}")

                # Checking if the bot has rights to pin the message.
                if context.bot.get_chat_member(chat_id, context.bot.id).can_pin_messages:
                    message.pin(disable_notification=False)
                # If the message should be pinned, but the bot hasn't got rights.
                elif queue.chat.notify:
                    update.effective_chat.send_message(**no_rights_to_pin_message())
            except Exception as e:
                logger.error(f"ERROR when creating queue: \n\t{queue} "
                             f"with message: \n{e}")
                update.effective_chat.send_message(**unexpected_error())
                message.delete()


@log_command('delete_queue')
@group_only_command
def delete_queue_command(update: Update, context: CallbackContext):
    """Handler for '/delete_queue <queue_name>' command"""

    chat_id = update.effective_chat.id
    queue_name = ' '.join(context.args)
    if not queue_name:
        logger.info("Deletion a queue with empty name.")
        update.effective_chat.send_message(**delete_queue_empty_name())
    else:
        session = create_session()
        queue: Queue = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).first()
        if queue is None:
            logger.info("Deletion nonexistent queue.")
            update.effective_chat.send_message(**queue_not_exist(queue_name=queue_name))
        else:
            session.delete(queue)
            session.commit()
            logger.info(f"Deleted queue: \n\t{queue}")
            update.effective_chat.send_message(**deleted_queue_message())

            if context.bot.get_chat_member(chat_id, context.bot.id).can_pin_messages:
                try:
                    context.bot.unpin_chat_message(chat_id, queue.message_id_to_edit)
                except BadRequest as e:
                    logger.error(f"ERROR when tried to unpin "
                                 f"message({queue.message_id_to_edit}) in queue({queue.queue_id}):\n\t"
                                 f"{e}")
            else:
                update.effective_chat.send_message(**no_rights_to_unpin_message())


@log_command('show_queues')
@group_only_command
def show_queues_command(update: Update, context: CallbackContext):
    """Handler for '/show_queues' command"""

    chat_id = update.effective_chat.id
    session = create_session()
    queues = session.query(Queue).filter(Queue.chat_id == chat_id).all()
    if not queues:
        update.effective_chat.send_message(**show_queues_message_empty())
    else:
        queue_names = [queue.name for queue in queues]
        update.effective_chat.send_message(**show_queues_message(queue_names))


@log_command('add_me')
@group_only_command
@__insert_queue_from_context(
    on_no_queue_log='Adding to queue with empty name',
    on_not_exist_log='Adding to nonexistent queue.',
    on_no_queue_reply=command_empty_queue_name(command_name='add_me')
)
def add_me_command(update: Update, context: CallbackContext, queue: Queue):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    session = create_session()
    member = (session
              .query(QueueMember)
              .filter(QueueMember.queue_id == queue.queue_id,
                      QueueMember.user_id == user_id).first())
    if member is not None:
        logger.info("Already in the queue.")
        update.effective_message.reply_text(**already_in_the_queue())
        return

    last_member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue.queue_id)
            .order_by(QueueMember.user_order.desc())
            .first()
    )
    if last_member is None:
        user_order = 1
    else:
        user_order = last_member.user_order + 1
    member = QueueMember(user_id=user_id, fullname=update.effective_user.full_name,
                         user_order=user_order, queue_id=queue.queue_id)
    session.add(member)
    session.commit()
    logger.info(f"Added member to queue: \n\t{member}")

    __edit_queue_members_message(queue, chat_id, context.bot)


@log_command('remove_me')
@group_only_command
@__insert_queue_from_context(
    on_no_queue_log='Removing from queue with empty name',
    on_not_exist_log='Removing from nonexistent queue',
    on_no_queue_reply=command_empty_queue_name(command_name='remove_me')
)
def remove_me_command(update: Update, context: CallbackContext, queue):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    session = create_session()
    member: QueueMember = (session
                           .query(QueueMember)
                           .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_id == user_id)
                           .first())
    if member is None:
        logger.info('Not yet in the queue')
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
            session.add(queue)
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

        __edit_queue_members_message(queue, chat_id, context.bot)


@log_command('skip_me')
@group_only_command
@__insert_queue_from_context(
    on_no_queue_log='Skipping with empty name',
    on_not_exist_log='Skipping turn from the nonexistent queue.',
    on_no_queue_reply=command_empty_queue_name('skip_me')
)
def skip_me_command(update: Update, context: CallbackContext, queue):
    chat_id = update.effective_chat.id
    session = create_session()

    member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue.queue_id,
                    QueueMember.user_id == update.effective_user.id)
            .first())
    if member is None:
        logger.info('Not yet in the queue')
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

            __edit_queue_members_message(queue, chat_id, context.bot)
        else:
            logging.info(f'Cancel skipping because of no other members in queue({queue.queue_id})')
            update.effective_message.reply_text(**cannot_skip())


@log_command('next')
@group_only_command
@__insert_queue_from_context(
    on_no_queue_log='Requested "next" with the empty queue name.',
    on_not_exist_log='Requested "next" with an nonexistent queue name.',
    on_no_queue_reply=command_empty_queue_name('next')
)
def next_command(update: Update, context: CallbackContext, queue):
    order = queue.current_order + 1
    queue.current_order = order

    session = create_session()
    member: QueueMember = (
        session
            .query(QueueMember)
            .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_order == queue.current_order)
            .first()
    )
    if member is None:
        logger.info(f"Reached the end of the queue({queue.queue_id})")
        update.effective_chat.send_message(**next_reached_queue_end())
    else:
        logging.info(f'Next member: {member}')
        update.effective_chat.send_message(**next_member_notify(member.fullname, member.user_id, queue.name))

        session.add(queue)
        session.commit()
        logger.info(f'Updated current_order: \n\t{queue}')

        __edit_queue_members_message(queue, update.effective_chat.id, context.bot)


@log_command('show_members')
@group_only_command
@__insert_queue_from_context(
    on_no_queue_log='Requested "show_members" command with the empty queue name',
    on_not_exist_log='Requested "show_members" with an nonexistent queue name.',
    on_no_queue_reply=command_empty_queue_name('show_members')
)
def show_members_command(update: Update, context: CallbackContext, queue):
    __show_members(update.effective_chat.id, queue, context.bot)


@log_command('notify_all')
@group_only_command
def notify_all_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    session = create_session()
    chat: Chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        if chat.notify:
            chat.notify = False
            session.commit()
            update.effective_chat.send_message(**notify_all_disabled_message())
        else:
            chat.notify = True
            session.commit()
            update.effective_chat.send_message(**notify_all_enabled_message())
        logger.info(f'Changed notify setting to {chat.notify} in chat({chat_id})')
    else:
        logging.error(f'Error fetching chat by chat_id({chat_id}) in active chat. '
                      'The chat must be in the DB, but doesn\'t.')


# noinspection PyUnusedLocal
@log_command('help')
def help_command(update: Update, context: CallbackContext):
    """Handler for '/help' command"""
    if update.effective_chat.type == 'private':
        update.effective_message.reply_text(**help_message())
    else:
        update.effective_message.reply_text(**help_message_in_chat())


# noinspection PyUnusedLocal
@log_command('about_me')
def about_me_command(update: Update, context: CallbackContext):
    """Handler for '/info' command"""
    update.effective_message.reply_text(**about_me_message())


# noinspection PyUnusedLocal
@log_command('unsupported_command')
def unsupported_command_handler(update: Update, context: CallbackContext):
    """Handler for any command, which doesn't exist in the bot."""
    update.effective_message.reply_text(**unknown_command())


# noinspection PyUnusedLocal
@log_command()
def unimplemented_command_handler(update: Update, context: CallbackContext):
    update.message.reply_text(**unimplemented_command())


def __show_members(chat_id: int, queue: Queue, bot):
    member_names = __get_queue_members(queue)
    message = bot.send_message(
        chat_id=chat_id,
        **show_queue_members(queue.name, member_names, queue.current_order)
    )
    if message:
        try:
            bot.delete_message(chat_id=chat_id, message_id=queue.message_id_to_edit)
        except BadRequest as e:
            logger.error(f'Error when deleting the previously sent message:')
            logger.error(e)
        queue.message_id_to_edit = message.message_id

        session = create_session()
        session.add(queue)
        session.commit()

        logger.info(f'Updated message_to_edit_id in queue:\n\t{queue}')


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


def __edit_queue_members_message(queue: Queue, chat_id: int, bot):
    member_names = __get_queue_members(queue)

    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=queue.message_id_to_edit,
            **show_queue_members(queue.name, member_names, queue.current_order)
        )
    except BadRequest as e:
        logger.error(f'ERROR when editing the message({queue.message_id_to_edit}) for queue({queue.queue_id}):')
        logger.error(e)
        logger.warning(f'Sending a new message for the queue({queue.queue_id}) because of the previous error.')

        __show_members(chat_id, queue, bot)
    logger.info(f'Edited message: chat_id={chat_id}, message_id={queue.message_id_to_edit}')


__all__ = [
    'start_command',
    'create_queue_command',
    'delete_queue_command',
    'show_queues_command',
    'add_me_command',
    'remove_me_command',
    'skip_me_command',
    'next_command',
    'show_members_command',
    'notify_all_command',
    'help_command',
    'about_me_command',
    'unsupported_command_handler',
    'unimplemented_command_handler'
]
