# Copyright (C) 2021 Vladyslav Synytsyn
"""All text constants related to the ``report_handler.py`` module."""

from typing import List

from telegram import ParseMode

from localization.buttons.keyboard_buttons import CancelKeyboardButtonText


class ReportMessagesStrings:
    # ## ENGLISH LOCALIZATION ## #
    __report_error_message_text_en = 'Describe the problem you encountered with, please: '
    __send_without_descr_keyb_btn_text_en = 'Send without description➡️'
    __thanks_for_feedback_text_en = (
        'Thanks for your feedback! \n'
        'My developer will take a look at the problem you described and will do his best to fix it.'
    )
    __thanks_for_feedback_without_descr_text_en = (
        'Thanks for your feedback. \n'
        'It will be _hard_ to know, _what_ was gone wrong, since you haven\'t added any _description_, '
        'but my developer will _take a look_ at this report and will _try_ to find out, how to satisfy it.'
    )
    __cancel_report_text_en = 'Okay, the report was cancelled.'

    # ## UKRAINIAN LOCALIZATION ## #
    __report_error_message_text_ukr = 'Опишіть, будь ласка, проблему, з якою Ви зіткнулися: '
    __send_without_descr_keyb_btn_text_ukr = 'Надіслати без опису ➡️'
    __thanks_for_feedback_text_ukr = (
        'Дякую за Ваш відгук! \n'
        'Мій розробник розгляне проблему, з якою Ви зіткнулися, і зробить усе можливе, щоб її виправити.'
    )
    __thanks_for_feedback_without_descr_text_ukr = (
        'Дякую за Ваш відгук. \n'
        'Буде _важко_ дізнатися, _що_ пішло не так, оскільки Ви не залишили жодного _опису_😠, '
        'але мій розробник _погляне_ на цей рапорт і _спробує_ зрозуміти, що можна було б зробити.'
    )
    __cancel_report_text_ukr = 'Гаразд, рапорт скасовано.'

    def __init__(self, language):
        """
        Args:
            language: The language, the text will be displayed in
        """
        self._lang = language

    def report_error_message(self):
        text: str
        if self._lang == 'en':
            text = ReportMessagesStrings.__report_error_message_text_en
        else:
            text = ReportMessagesStrings.__report_error_message_text_ukr
        return {'text': text}

    def get_keyboard_for_report(self) -> List[List[str]]:
        keyboard_button_text = CancelKeyboardButtonText(self._lang)
        keyboard: List[List[str]]
        if self._lang == 'en':
            keyboard = [
                [ReportMessagesStrings.__send_without_descr_keyb_btn_text_en],
                [keyboard_button_text.get_cancel_button_text()]
            ]
        else:
            keyboard = [
                [ReportMessagesStrings.__send_without_descr_keyb_btn_text_ukr],
                [keyboard_button_text.get_cancel_button_text()]
            ]
        return keyboard

    def thanks_for_feedback_message(self):
        text: str
        if self._lang == 'en':
            text = ReportMessagesStrings.__thanks_for_feedback_text_en
        else:
            text = ReportMessagesStrings.__thanks_for_feedback_text_ukr
        return {'text': text}

    def thanks_for_feedback_without_description_message(self):
        text: str
        if self._lang == 'en':
            text = ReportMessagesStrings.__thanks_for_feedback_without_descr_text_en
        else:
            text = ReportMessagesStrings.__thanks_for_feedback_without_descr_text_ukr
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def cancel_report_message(self):
        text: str
        if self._lang == 'en':
            text = ReportMessagesStrings.__cancel_report_text_en
        else:
            text = ReportMessagesStrings.__cancel_report_text_ukr
        return {'text': text}

    @staticmethod
    def get_all_without_description_texts():
        return [
            ReportMessagesStrings.__send_without_descr_keyb_btn_text_en,
            ReportMessagesStrings.__send_without_descr_keyb_btn_text_ukr
        ]
