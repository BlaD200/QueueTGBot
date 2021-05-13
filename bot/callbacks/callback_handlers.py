import json
from typing import Callable, Any

from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger
from app_logging.handler_logging import log_command
from bot.callbacks.message_buttons import get_member_action_buttons
from bot.constants import CACHE_TIME
from bot.controller.member_controller import add_me_action, remove_me_action, skip_me_action, \
    next_action
from localization.replies import deleted_queue_message, callback_empty_queue_id, callback_empty_queue_id__for_pin, \
    show_queue_members, no_rights_to_pin_message
from sql import create_session
from sql.domain import Queue


logger = get_logger(__name__)


def __insert_queue_from_callback_data(on_no_queue_log: str, on_not_exist_log: str, on_no_queue_reply: dict):
    def insert_queue_from_callback_data_decorator_maker(
            callback_handler_function: Callable[[Update, CallbackContext, Queue], Any]
    ):
        def insert_queue_from_callback_data_wrapper(update: Update, context: CallbackContext):
            query = update.callback_query
            data = json.loads(query.data)
            session = create_session()
            queue = (session
                     .query(Queue)
                     .filter(Queue.queue_id == data['queue_id'])
                     .first())

            if queue:
                return callback_handler_function(update, context, queue)
            # The id was specified but queue with this id wasn't found in DB
            elif not queue and data['queue_id']:
                logger.info(on_not_exist_log)
                update.callback_query.answer(**deleted_queue_message(), cache_time=CACHE_TIME)
            else:
                logger.warning(on_no_queue_log)
                update.callback_query.answer(**on_no_queue_reply, cache_time=CACHE_TIME)

        return insert_queue_from_callback_data_wrapper

    return insert_queue_from_callback_data_decorator_maker


@log_command("add_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Queue id wasn\'t found in callback data',
    on_not_exist_log='Adding to nonexistent or deleted queue.',
    on_no_queue_reply=callback_empty_queue_id(command_name='add_me')
)
def add_me_callback(update: Update, context: CallbackContext, queue: Queue):
    add_me_action(update, queue, context.bot)


@log_command("remove_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Removing from queue with empty name',
    on_not_exist_log='Removing from nonexistent queue',
    on_no_queue_reply=callback_empty_queue_id(command_name='add_me')
)
def remove_me_callback(update: Update, context: CallbackContext, queue: Queue):
    remove_me_action(update, queue, context.bot)


@log_command("skip_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Skipping with empty name',
    on_not_exist_log='Skipping turn from the nonexistent queue.',
    on_no_queue_reply=callback_empty_queue_id('skip_me')
)
def skip_me_callback(update: Update, context: CallbackContext, queue: Queue):
    skip_me_action(update, queue, context.bot)


@log_command("next_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Requested "next" with the empty queue name.',
    on_not_exist_log='Requested "next" with an nonexistent queue name.',
    on_no_queue_reply=callback_empty_queue_id('next')
)
def next_callback(update: Update, context: CallbackContext, queue: Queue):
    next_action(update, queue, context.bot)


@log_command('pin_queue')
@__insert_queue_from_callback_data(
    on_no_queue_log='Trying to pin queue with empty queue name.',
    on_not_exist_log='Trying to pin a nonexistent queue.',
    on_no_queue_reply=callback_empty_queue_id__for_pin()
)
def pin_queue_callback(update: Update, context: CallbackContext, queue: Queue):
    bot = context.bot
    # Checking if the bot has rights to pin the message.
    if bot.get_chat_member(queue.chat_id, bot.id).can_pin_messages:
        bot.pin_chat_message(chat_id=queue.chat_id, message_id=queue.message_id_to_edit)
        logger.info(f"Queue({queue.queue_id}) was pinned in chat({queue.chat_id})")
        update.callback_query.answer()
    # If the message should be pinned, but the bot hasn't got rights.
    elif queue.chat.notify:
        update.callback_query.answer(no_rights_to_pin_message()['text'])

    context.bot.edit_message_text(
        chat_id=queue.chat_id,
        message_id=queue.message_id_to_edit,
        **show_queue_members(queue.name),
        **get_member_action_buttons(queue.queue_id)
    )
    logger.info(f"Pin button was removed for queue({queue.queue_id})")
