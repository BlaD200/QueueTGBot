# Copyright (C) 2021 Vladyslav Synytsyn
"""This module contains the functions that handle all commands supported by the bot."""

import logging
from typing import Optional, List, Callable, Any

from sqlalchemy.orm import joinedload
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackContext, ConversationHandler

import app_logging
from app_logging.handler_logging import log_command
from bot.callbacks.message_buttons import show_members_buttons
from bot.chat_type_accepted import group_only_handler
from bot.controller.member_controller import add_me_action, remove_me_action, next_action, \
    skip_me_action
from localization.keyboard_buttons import get_cancel_button_text
from localization.replies import (
    start_message_private, start_message_chat,
    unknown_command, unimplemented_command,
    create_queue_exist, help_message_private, help_message_in_chat,
    about_me_message,
    unexpected_error, queue_not_exist, deleted_queue_message, show_queues_message_empty,
    show_queues_message, command_empty_queue_name, show_queue_members, no_rights_to_pin_message,
    reply_to_wrong_message_message,
    no_rights_to_unpin_message, notify_all_disabled_message, notify_all_enabled_message, enter_queue_name_message,
    cancel_queue_creation_message, queue_created_remove_keyboard_message
)
from sql import create_session
from sql.domain import *


# Registering logger here
logger: logging.Logger = app_logging.get_logger(__name__)


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

    def insert_queue_from_context_decorator_maker(
            command_handler_function: Callable[[Update, CallbackContext, Queue], Any]):
        def insert_queue_from_context_wrapper(update: Update, context: CallbackContext):
            chat_id = update.effective_chat.id
            queue: Optional[Queue] = None

            session = create_session()
            # Trying to get the queue from message_id, that user replied to.
            if update.effective_message.reply_to_message:
                replied_message_id = update.effective_message.reply_to_message.message_id
                logger.info(f'Replied to message({replied_message_id})')
                queue = (session
                         .query(Queue)
                         .filter(Queue.chat_id == chat_id, Queue.message_id_to_edit == replied_message_id)
                         .options(joinedload(Queue.members))
                         .first())
                # User replied to the wrong message (not with members) or to deleted queue.
                if not queue:
                    logger.info('Replied to wrong message or to the deleted queue.')
                    update.effective_message.reply_text(**reply_to_wrong_message_message())
                    return

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

        return insert_queue_from_context_wrapper

    return insert_queue_from_context_decorator_maker


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
        logger.info(f'Start command in group: \n\t{update.effective_chat}')
        update.effective_message.reply_text(
            **start_message_chat(fullname=update.message.from_user.full_name,
                                 user_id=update.message.from_user.id)
        )


### CREATE QUEUE ###
QUEUE_NAME = 1


@log_command('create_queue')
@group_only_handler
def create_queue_command(update: Update, context: CallbackContext):
    """Handler for '/create_queue <queue_name>' command"""

    queue_name = ' '.join(context.args)
    if not queue_name:
        # logger.info("Creation a queue with empty name.")
        # update.effective_chat.send_message(**create_queue_empty_name())
        update.effective_message.reply_text(
            **enter_queue_name_message(),
            reply_markup=ReplyKeyboardMarkup(
                [[get_cancel_button_text()]],
                one_time_keyboard=True, resize_keyboard=True, selective=True),
        )
        return QUEUE_NAME

    else:
        create_queue_action(update, queue_name, context.bot)
        return ConversationHandler.END


def create_queue_name_handler(update: Update, context: CallbackContext):
    queue_name = update.effective_message.text

    create_queue_action(update, queue_name, context.bot)
    return ConversationHandler.END


def cancel_queue_creation_handler(update: Update, context: CallbackContext) -> int:
    """Handler for the ``cancel_keyboard_button`` button."""
    logger.info(f'Queue creation was cancelled by the user({update.effective_user.id})')
    update.effective_message.reply_text(**cancel_queue_creation_message(),
                                        reply_markup=ReplyKeyboardRemove(selective=True))

    return ConversationHandler.END


def create_queue_action(update: Update, queue_name: str, bot):
    chat_id = update.effective_chat.id

    session = create_session()
    count = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).count()
    if count == 1:
        logger.info("Creating a queue with an existing name")
        update.effective_message.reply_text(
            **create_queue_exist(queue_name=queue_name), reply_markup=ReplyKeyboardRemove(selective=True)
        )
    else:
        queue = Queue(name=queue_name, chat_id=chat_id)
        message = None
        try:
            session.add(queue)
            session.commit()

            message = update.effective_chat.send_message(**show_members_buttons(queue.queue_id, queue_name))

            queue.message_id_to_edit = message.message_id
            session.merge(queue)
            session.commit()

            logger.info(f"New queue created: \n\t{queue}")

            # Send the reply to hide the keyboard for the user if one was present
            if update.effective_message.reply_markup:
                message = update.effective_message.reply_text(
                    **queue_created_remove_keyboard_message(),
                    reply_markup=ReplyKeyboardRemove(selective=True)
                )
                message.delete()

            # Checking if the bot has rights to pin the message.
            if bot.get_chat_member(chat_id, bot.id).can_pin_messages:
                if queue.chat.notify:
                    message.pin()
            # If the message should be pinned, but the bot hasn't got rights.
            elif queue.chat.notify:
                update.effective_chat.send_message(**no_rights_to_pin_message())
        except Exception as e:
            logger.exception(f"ERROR when creating queue: \n\t{queue} "
                             f"with message: \n{e}")
            update.effective_chat.send_message(**unexpected_error())
            if message:
                message.delete()


####################


@log_command('delete_queue')
@group_only_handler
def delete_queue_command(update: Update, context: CallbackContext):
    """Handler for '/delete_queue <queue_name>' command"""

    queue_name = ' '.join(context.args)
    if not queue_name:
        # TODO suggest all queues in the keyboard
        # logger.info("Deletion a queue with empty name.")
        # update.effective_chat.send_message(**delete_queue_empty_name())
        update.effective_message.reply_text(
            **enter_queue_name_message(),
            reply_markup=ReplyKeyboardMarkup(
                [[get_cancel_button_text()]],
                one_time_keyboard=True, resize_keyboard=True, selective=True),
        )
        return QUEUE_NAME
    else:
        delete_queue_action(update, queue_name, context.bot)
        return ConversationHandler.END


def delete_queue_name_handler(update: Update, context: CallbackContext):
    queue_name = update.effective_message.text
    delete_queue_action(update, queue_name, context.bot)
    return ConversationHandler.END


def cancel_queue_deletion_handler(update: Update, context: CallbackContext) -> int:
    """Handler for the ``cancel_keyboard_button`` button."""
    logger.info(f'Queue deletion was cancelled by the user({update.effective_user.id})')
    update.effective_message.reply_text(**cancel_queue_creation_message(),
                                        reply_markup=ReplyKeyboardRemove(selective=True))

    return ConversationHandler.END


def delete_queue_action(update: Update, queue_name: str, bot):
    chat_id = update.effective_chat.id

    session = create_session()
    queue: Queue = session.query(Queue).filter(Queue.chat_id == chat_id, Queue.name == queue_name).first()
    if queue is None:
        logger.info("Deletion nonexistent queue.")
        update.effective_chat.send_message(
            **queue_not_exist(queue_name=queue_name),
            reply_markup=ReplyKeyboardRemove(selective=True)
        )
    else:
        session.delete(queue)
        session.commit()
        logger.info(f"Deleted queue: \n\t{queue}")
        # TODO silent
        update.effective_message.reply_text(
            **deleted_queue_message(),
            reply_markup=ReplyKeyboardRemove(selective=True)
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
            update.effective_chat.send_message(**no_rights_to_unpin_message())


@log_command('show_queues')
@group_only_handler
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
@group_only_handler
@__insert_queue_from_context(
    on_no_queue_log='Adding to queue with empty name',
    on_not_exist_log='Adding to nonexistent queue.',
    on_no_queue_reply=command_empty_queue_name(command_name='add_me')
)
def add_me_command(update: Update, context: CallbackContext, queue: Queue):
    add_me_action(update, queue, context.bot)


@log_command('remove_me')
@group_only_handler
@__insert_queue_from_context(
    on_no_queue_log='Removing from queue with empty name',
    on_not_exist_log='Removing from nonexistent queue',
    on_no_queue_reply=command_empty_queue_name(command_name='remove_me')
)
def remove_me_command(update: Update, context: CallbackContext, queue: Queue):
    remove_me_action(update, queue, context.bot)


@log_command('skip_me')
@group_only_handler
@__insert_queue_from_context(
    on_no_queue_log='Skipping with empty name',
    on_not_exist_log='Skipping turn from the nonexistent queue.',
    on_no_queue_reply=command_empty_queue_name('skip_me')
)
def skip_me_command(update: Update, context: CallbackContext, queue):
    skip_me_action(update, queue, context.bot)


@log_command('next')
@group_only_handler
@__insert_queue_from_context(
    on_no_queue_log='Requested "next" with the empty queue name.',
    on_not_exist_log='Requested "next" with an nonexistent queue name.',
    on_no_queue_reply=command_empty_queue_name('next')
)
def next_command(update: Update, context: CallbackContext, queue):
    next_action(update, queue, context.bot)


@log_command('show_members')
@group_only_handler
@__insert_queue_from_context(
    on_no_queue_log='Requested "show_members" command with the empty queue name',
    on_not_exist_log='Requested "show_members" with an nonexistent queue name.',
    on_no_queue_reply=command_empty_queue_name('show_members')
)
def show_members_command(update: Update, context: CallbackContext, queue):
    __show_members(update.effective_chat.id, queue, context.bot)


@log_command('notify_all')
@group_only_handler
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
        update.effective_message.reply_text(**help_message_private())
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
            logger.exception(f'Error when deleting the previously sent message: {e}')
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
        logger.exception(f'ERROR when editing the message({queue.message_id_to_edit}) for queue({queue.queue_id}): \n\t'
                         f'{e}')
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
