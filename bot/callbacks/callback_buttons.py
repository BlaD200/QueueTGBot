import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app_logging import get_logger
from bot.callbacks.callback_data_actions import *
from localization.buttons.callback_buttons_text import QueueMemberCallbackButtonsText, SelectLanguageCallbackButtonsText


logger = get_logger(__name__)


def get_member_action_buttons(queue_id, language, add_notify_button=False):
    data_add = {'action': ADD_ME, 'queue_id': queue_id}
    data_remove = {'action': REMOVE_ME, 'queue_id': queue_id}
    data_skip = {'action': SKIP_ME, 'queue_id': queue_id}
    data_next = {'action': NEXT, 'queue_id': queue_id}
    data_notify = {'action': NOTIFY, 'queue_id': queue_id}
    data_go_end = {'action': GO_END, 'queue_id': queue_id}

    callback_buttons_text = QueueMemberCallbackButtonsText(language)

    keyboard = [
        [InlineKeyboardButton(callback_buttons_text.next_text(), callback_data=json.dumps(data_next))],
        [
            InlineKeyboardButton(callback_buttons_text.add_me_text(), callback_data=json.dumps(data_add)),
            InlineKeyboardButton(callback_buttons_text.remove_me_text(), callback_data=json.dumps(data_remove))
        ],
        [
            InlineKeyboardButton(callback_buttons_text.skip_me_text(), callback_data=json.dumps(data_skip)),
            InlineKeyboardButton(callback_buttons_text.move_me_to_the_end(), callback_data=json.dumps(data_go_end)),
        ]
    ]
    if add_notify_button:
        keyboard.append(
            [InlineKeyboardButton(callback_buttons_text.notify_text(), callback_data=json.dumps(data_notify))])

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
