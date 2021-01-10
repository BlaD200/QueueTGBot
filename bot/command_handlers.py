"""This module contains the functions that handle all commands supported by the bot."""

import logging

from sqlalchemy import text
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
    show_queues_message, command_empty_queue_name, show_queue_members, already_in_the_queue, no_rights_to_pin_message
)
from sql import create_session
from sql.domain import *


# Registering logger here
logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)
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
                logging.info(f"{_command_name}: [{info}] edited")
            else:
                logging.info(f"{_command_name} [{info}]")

            return f(update, context)

        return wrapped

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
        update.effective_message.reply_text(
            **start_message_private(fullname=update.message.from_user.full_name)
        )
    else:
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
            queue = Queue(name=queue_name, notify=True, chat_id=chat_id)
            try:
                message = update.effective_chat.send_message(**show_queue_members(queue_name))
                queue.message_id_to_edit = message.message_id

                session.add(queue)
                session.commit()
                logger.info(f"New queue created: \n\t{queue}")

                try:
                    message.pin(disable_notification=False)
                except BadRequest:
                    update.effective_chat.send_message(**no_rights_to_pin_message())
            except Exception as e:
                logger.error(f"ERROR when creating queue: \n\t{queue} "
                             f"with message: \n{e}")
                update.effective_chat.send_message(**unexpected_error())


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
            logger.info("Deletion inexistent queue.")
            update.effective_chat.send_message(**queue_not_exist(queue_name=queue_name))
        else:
            session.delete(queue)
            session.commit()
            logger.info(f"Deleted queue: \n\t{queue}")
            update.effective_chat.send_message(**deleted_queue_message())


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


def _edit_queue_members_message(queue: Queue, chat_id: int, bot):
    session = create_session()
    members = session.query(QueueMember).filter(QueueMember.queue_id == queue.queue_id).all()
    member_names = [member.fullname for member in members]
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=queue.message_id_to_edit,
        **show_queue_members(queue.name, member_names)
    )
    logger.info(f'Edited message: chat_id={chat_id}, message_id={queue.message_id_to_edit}')


@log_command('add_me')
@group_only_command
def add_me_command(update: Update, context: CallbackContext):
    queue_name = ' '.join(context.args)
    if not queue_name:
        logger.info('Adding to queue with empty name')
        update.effective_chat.send_message(**command_empty_queue_name(command_name='add_me'))
        return

    chat_id = update.effective_chat.id
    session = create_session()
    queue = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).first()
    if queue is None:
        logger.info('Adding to inexistent queue.')
        update.effective_message.reply_text(**queue_not_exist(queue_name=queue_name))
    else:
        user_id = update.effective_user.id
        member = (session
                  .query(QueueMember)
                  .filter(QueueMember.queue_id == queue.queue_id,
                          QueueMember.user_id == user_id).first())
        if member is not None:
            logger.info("Already in the queue.")
            update.effective_message.reply_text(**already_in_the_queue())
            return

        order = queue.current_order + 1
        queue.current_order = order
        member = QueueMember(user_id=user_id, fullname=update.effective_user.full_name,
                             user_order=queue.current_order, queue_id=queue.queue_id)
        session.add_all([member, queue])
        session.commit()
        logger.info(f"Added member to queue: \n\t{member}")

        _edit_queue_members_message(queue, chat_id, context.bot)


@log_command('remove_me')
@group_only_command
def remove_me_command(update: Update, context: CallbackContext):
    queue_name = ''.join(context.args)
    if not queue_name:
        logger.info('Removing fom queue with empty name')
        update.effective_message.reply_text(command_empty_queue_name(command_name='remove_me'))

    chat_id = update.effective_chat.id
    session = create_session()
    queue = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).first()
    if queue is None:
        logger.info('Removing from inexistent queue')
        update.effective_message.reply_text(**queue_not_exist(queue_name))
    else:
        user_id = update.effective_user.id
        member: QueueMember = (session
                               .query(QueueMember)
                               .filter(QueueMember.queue_id == queue.queue_id, QueueMember.user_id == user_id)
                               .first())
        if member is None:
            logger.info('Not yet in the queue')
            ...
        else:
            session.delete(member)
            # Updating user_order in queue_members table
            # to move down all users with user_order greater than the value of deleted user
            update_stmt: TextClause = text('UPDATE queue_member '
                                           'SET user_order = user_order - 1 '
                                           'WHERE user_order > :deleted_user_order;')
            session.execute(update_stmt, {'deleted_user_order': member.user_order})
            # Updating current order in queue
            queue.current_order = queue.current_order - 1
            session.add(queue)

            session.commit()

            logger.info(f'User removed from queue (queue_id={queue.queue_id})')
            logger.info(f'Updated user_order in queue({queue.queue_id}) for users(order>{member.user_order})')

            _edit_queue_members_message(queue, chat_id, context.bot)


@log_command('help')
def help_command(update: Update, context: CallbackContext):
    """Handler for '/help' command"""
    if update.effective_chat.type == 'private':
        update.effective_message.reply_text(**help_message())
    else:
        update.effective_message.reply_text(**help_message_in_chat())


@log_command('about_me')
def about_me_command(update: Update, context: CallbackContext):
    """Handler for '/info' command"""
    update.effective_message.reply_text(**about_me_message())


@log_command('unsupported_command')
def unsupported_command_handler(update: Update, context: CallbackContext):
    """Handler for any command, which doesn't exist in the bot."""
    update.effective_message.reply_text(**unknown_command())


@log_command()
def unimplemented_command_handler(update: Update, context: CallbackContext):
    update.message.reply_text(**unimplemented_command())


__all__ = [
    'start_command',
    'create_queue_command',
    'delete_queue_command',
    'show_queues_command',
    'help_command',
    'about_me_command',
    'unsupported_command_handler',
    'unimplemented_command_handler'
]
