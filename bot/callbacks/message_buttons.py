import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app_logging import get_logger
from bot.callbacks.callback_data_actions import *
from localization.buttons_text import ButtonsText
from localization.replies import show_queue_members


logger = get_logger(__name__)


def show_members_buttons(queue_id, queue_name):
    data_add = {'action': ADD_ME, 'queue_id': queue_id}
    data_remove = {'action': REMOVE_ME, 'queue_id': queue_id}
    data_skip = {'action': SKIP_ME, 'queue_id': queue_id}
    data_next = {'action': NEXT, 'queue_id': queue_id}

    keyboard = [
        [InlineKeyboardButton(ButtonsText.next_text(), callback_data=json.dumps(data_next))],
        [
            InlineKeyboardButton(ButtonsText.add_me_text(), callback_data=json.dumps(data_add)),
            InlineKeyboardButton(ButtonsText.skip_me_text(), callback_data=json.dumps(data_skip)),
            InlineKeyboardButton(ButtonsText.remove_me_text(), callback_data=json.dumps(data_remove))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return {**show_queue_members(queue_name), 'reply_markup': reply_markup}
