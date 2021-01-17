"""All text constants related to the ``report_handler.py`` module."""

from typing import List

from telegram import ParseMode


def report_error_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Describe the problem you encountered with, please: '
    else:
        text = "TODO"
    return {'text': text}


def get_keyboard_for_report(lang: str = 'en') -> List[List[str]]:
    keyboard: List[List[str]]
    if lang == 'en':
        keyboard = [['Send without description➡️'], ['Cancel❌']]
    else:
        keyboard = [['TODO']]
    return keyboard


def thanks_for_feedback_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Thanks for your feedback! \n' \
               'My developer will take a look at the problem you described and will do his best to fix it.'
    else:
        text = "TODO"
    return {'text': text}


def thanks_for_feedback_without_description_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Thanks for your feedback. \n' \
               'It will be _hard_ to know, _what_ was gone wrong, since you haven\'t added any _description_, ' \
               'but my developer will _take a look_ at this report and will _try_ to find out, how to satisfy it.'
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def cancel_report_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Okay, the report was cancelled.'
    else:
        text = "TODO"
    return {'text': text}
