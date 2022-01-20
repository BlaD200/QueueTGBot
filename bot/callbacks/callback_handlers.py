import json
from typing import Callable, Any, Union

from telegram import Update
from telegram.ext import CallbackContext

from app_logging import get_logger, BotCachingHandler
from app_logging.handler_logging import log_command
from bot.callbacks.callback_buttons import get_member_action_buttons, ENG_LANGUAGE
from bot.constants import CACHE_TIME
from bot.controller.member_controller import add_me_action, remove_me_action, skip_me_action, \
    next_action
from localization import QueueActionsStrings, SettingsStrings, UnwantedBehaviourStrings
from sql import create_session
from sql.domain import Queue, Chat


logger = get_logger(__name__)


def __insert_queue_from_callback_data(on_no_queue_log: str, on_not_exist_log: str,
                                      on_no_queue_reply_callable: Callable[[str, str], dict],
                                      on_no_queue_reply_args: Union[str, None] = None):
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
                strings = QueueActionsStrings(queue.chat.language)
                update.callback_query.answer(**strings.deleted_queue_message(), cache_time=CACHE_TIME)
            else:
                logger.warning(on_no_queue_log)
                session = create_session()
                chat = session.query(Chat).filter(Chat.chat_id == update.effective_chat.id).first()
                lang = chat.language
                reply = on_no_queue_reply_callable(on_no_queue_reply_args, lang)
                update.callback_query.answer(reply['text'], cache_time=CACHE_TIME)

        return insert_queue_from_callback_data_wrapper

    return insert_queue_from_callback_data_decorator_maker


@log_command("add_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Queue id wasn\'t found in callback data',
    on_not_exist_log='Adding to nonexistent or deleted queue.',
    on_no_queue_reply_callable=QueueActionsStrings('en').callback_empty_queue_id,
    on_no_queue_reply_args='add_me'
)
def add_me_callback(update: Update, context: CallbackContext, queue: Queue):
    add_me_action(update, queue, context.bot)


@log_command("remove_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Removing from queue with empty name',
    on_not_exist_log='Removing from nonexistent queue',
    on_no_queue_reply_callable=QueueActionsStrings('en').callback_empty_queue_id, on_no_queue_reply_args='remove_me'
)
def remove_me_callback(update: Update, context: CallbackContext, queue: Queue):
    remove_me_action(update, queue, context.bot)


@log_command("skip_me_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Skipping with empty name',
    on_not_exist_log='Skipping turn from the nonexistent queue.',
    on_no_queue_reply_callable=QueueActionsStrings('en').callback_empty_queue_id, on_no_queue_reply_args='skip_me'
)
def skip_me_callback(update: Update, context: CallbackContext, queue: Queue):
    skip_me_action(update, queue, context.bot)


@log_command("next_callback")
@__insert_queue_from_callback_data(
    on_no_queue_log='Requested "next" with the empty queue name.',
    on_not_exist_log='Requested "next" with an nonexistent queue name.',
    on_no_queue_reply_callable=QueueActionsStrings('en').callback_empty_queue_id, on_no_queue_reply_args='next'
)
def next_callback(update: Update, context: CallbackContext, queue: Queue):
    next_action(update, queue, context.bot)


@log_command('pin_queue')
@__insert_queue_from_callback_data(
    on_no_queue_log='Trying to pin queue with empty queue name.',
    on_not_exist_log='Trying to pin a nonexistent queue.',
    on_no_queue_reply_callable=QueueActionsStrings('en').callback_empty_queue_id__for_pin
)
def pin_queue_callback(update: Update, context: CallbackContext, queue: Queue):
    bot = context.bot
    # Checking if the bot has rights to pin the message.
    if bot.get_chat_member(queue.chat_id, bot.id).can_pin_messages:
        bot.pin_chat_message(chat_id=queue.chat_id, message_id=queue.message_id_to_edit)
        logger.info(f"Queue({queue.queue_id}) was pinned in chat({queue.chat_id})")
        update.callback_query.answer()
    # If the message should be pinned, but the bot hasn't got rights.
    else:
        strings = UnwantedBehaviourStrings(queue.chat.language)
        update.callback_query.answer(strings.no_rights_to_pin_message()['text'], show_alert=True)

    strings = QueueActionsStrings(queue.chat.language)
    context.bot.edit_message_text(
        chat_id=queue.chat_id,
        message_id=queue.message_id_to_edit,
        **strings.show_queue_members(queue.name),
        **get_member_action_buttons(queue.queue_id, queue.chat.language)
    )
    logger.info(f"Pin button was removed for queue({queue.queue_id})")


@log_command('language_callback')
def language_setup_for_chat_callback(update: Update, context: CallbackContext):
    data = json.loads(update.callback_query.data)
    lang = 'en' if data['action'] == ENG_LANGUAGE else 'ukr'
    session = create_session()
    chat_id = update.effective_chat.id
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()

    error_strings = UnwantedBehaviourStrings(chat.language)
    if chat:
        try:
            chat.language = lang
            session.commit()
            logger.info(f"Chat({chat.chat_id}) language was changed to {lang}.")
            update.callback_query.answer()
            strings = SettingsStrings(language=lang)
            context.bot.send_message(chat_id=chat_id, **strings.chat_language_setting())
        except Exception as e:
            logger.exception(f"ERROR when changing language for chat({chat}) "
                             f"with message: \n{e}")
            update.callback_query.answer()
            update.effective_chat.send_message(**error_strings.unexpected_error())
    else:
        logger.error(f"ERROR when changing language for chat_id({chat_id}). Chat wasn't found in DB. ",
                     extra={BotCachingHandler.flash_to_bot: True,
                            BotCachingHandler.error_from_chat_id: chat_id,
                            BotCachingHandler.error_description: 'Chat wan\'t found in DB when processing '
                                                                 'language setup callback.'}
                     )
        update.callback_query.answer()
        update.effective_chat.send_message(**error_strings.unexpected_error_with_report())
