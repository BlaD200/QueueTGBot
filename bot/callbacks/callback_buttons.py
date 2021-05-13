import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app_logging import get_logger
from bot.callbacks.callback_data_actions import *
from localization.callback_buttons_text import QueueMemberCallbackButtonsText, SelectLanguageCallbackButtonsText


logger = get_logger(__name__)


def get_member_action_buttons(queue_id, add_notify_button=False):
    data_add = {'action': ADD_ME, 'queue_id': queue_id}
    data_remove = {'action': REMOVE_ME, 'queue_id': queue_id}
    data_skip = {'action': SKIP_ME, 'queue_id': queue_id}
    data_next = {'action': NEXT, 'queue_id': queue_id}
    data_notify = {'action': NOTIFY, 'queue_id': queue_id}

    keyboard = [
        [InlineKeyboardButton(QueueMemberCallbackButtonsText.next_text(), callback_data=json.dumps(data_next))],
        [
            InlineKeyboardButton(QueueMemberCallbackButtonsText.add_me_text(), callback_data=json.dumps(data_add)),
            InlineKeyboardButton(QueueMemberCallbackButtonsText.skip_me_text(), callback_data=json.dumps(data_skip)),
            InlineKeyboardButton(QueueMemberCallbackButtonsText.remove_me_text(), callback_data=json.dumps(data_remove))
        ],
    ]
    if add_notify_button:
        keyboard.append(
            [InlineKeyboardButton(QueueMemberCallbackButtonsText.notify_text(), callback_data=json.dumps(data_notify))])

    reply_markup = InlineKeyboardMarkup(keyboard)

    return {'reply_markup': reply_markup}


def get_language_select_buttons():
    data_eng_lang = {'action': ENG_LANGUAGE}
    data_urk_lang = {'action': URK_LANGUAGE}

    keyboard = [
        [
            InlineKeyboardButton(SelectLanguageCallbackButtonsText.english_language_text(),
                                 callback_data=json.dumps(data_eng_lang)),
            InlineKeyboardButton(SelectLanguageCallbackButtonsText.ukrainian_language_text(),
                                 callback_data=json.dumps(data_urk_lang)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return {'reply_markup': reply_markup}
