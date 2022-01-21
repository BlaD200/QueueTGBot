from telegram import ParseMode

from localization.base_localization import BaseLocalization


class SettingsStrings(BaseLocalization):
    # ## ENGLISH LOCALIZATION ## #
    __notify_all_disabled_message_text_en = (
        'The messages with new queues *will not* be pinned more.\n\n'
        '_And members in this chat will not be notified when a new queue will be created..._'
    )
    __notify_all_enabled_message_text_en = (
        'The messages with new queues *will be* pinned!\n\n'
    )
    __silent_mode_enabled_message_text_en = (
        '_Silent mode on_\. \n\n'
        'All unrequired messages *won\'t* be sent, including *help* messages\. '
        'Be sure, you know how to use the bot\.'
    )
    __silent_mode_disabled_message_text_en = (
        '_Silent mode off_\. \n\n'
        'All help and additional messages *will be* sent to give more detailed feedback\. '
        'If you already know all aspects of the bot, you could turn it off\.'
    )
    __select__language_message_text_en = (
        'Please, select the language, in which i will speak'
    )
    __chat__language_setting_text_en = (
        "👍Okay, now I'll speak *English*🇬🇧 in this chat\. Good luck😉"
    )

    # ## UKRAINIAN LOCALIZATION ## #
    __notify_all_disabled_message_text_ukr = (
        'Повідомлення з новими чергами більше *не будуть* закріплюватися.\n\n'
        "_Тож учасники цього чату не зможуть дізнатися, коли з'явиться нова черга..._"
    )
    __notify_all_enabled_message_text_ukr = (
        'Тепер нові черги *будуть закріплюватися*!'
    )
    __silent_mode_enabled_message_text_ukr = (
        '_Режим тиші увімкнено_\. \n\n'
        "Усі необов\'язкові повідомлення *не будуть* надсилатися, включаючи підсказки та додаткові повідомлення\."
    )
    __silent_mode_disabled_message_text_ukr = (
        "_Режим тиші вимкнено_\.\n\n"
        "Я буду підказувати, як користуватися командами, та скажу, якщо щось піде не так🤗\.\n"
        "Якщо Ви вже знаєте, як зі мною працювати та не потребуєте підсказок, то можете сміливо вмикати цей режим\.😊"
    )
    __select__language_message_text_ukr = (
        'Виберіть, будь ласка, якою мовою я буду спілкуватися'
    )
    __chat__language_setting_text_ukr = (
        "👍Добре, тепер я буду використовувати *Українську*🇺🇦 у цьому чаті\. Насолоджуйтеся😉"
    )

    def notify_all_enabled_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__notify_all_enabled_message_text_ukr
        else:
            text = self.__notify_all_enabled_message_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def notify_all_disabled_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__notify_all_disabled_message_text_ukr
        else:
            text = self.__notify_all_disabled_message_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def silent_mode_enabled_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__silent_mode_enabled_message_text_ukr
        else:
            text = self.__silent_mode_enabled_message_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def silent_mode_disabled_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__silent_mode_disabled_message_text_ukr
        else:
            text = self.__silent_mode_disabled_message_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def select_language_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__select__language_message_text_ukr
        else:
            text = self.__select__language_message_text_en
        return {'text': text}

    def chat_language_setting(self):
        """"""
        text: str
        if self._lang == 'ukr':
            text = self.__chat__language_setting_text_ukr
        else:
            text = self.__chat__language_setting_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}
