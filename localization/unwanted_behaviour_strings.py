from telegram import ParseMode

from localization.base_localization import BaseLocalization


class UnwantedBehaviourStrings(BaseLocalization):
    # ## ENGLISH LOCALIZATION ## #
    __no_rights_to_pin_message_text_en = (
        "I have no rights to pin this message.😢😒\n"
        "Give me this permission or ask your admin👮‍♂️ to pin manually."
    )
    __no_rights_to_unpin_message_text_en = (
        "I would unpin that queue with pleasure, but you didn't give me the necessary rights.😢😒\n"
        "Give me this permission or ask your admin👮‍♂️ to unpin manually."
    )
    __unknown_command_text_en = (
        "Unknown command.😧 \n"
        "To see the help type /help or type '/' to see the hints for commands, "
        "press tab and complete selected command by adding required arguments."
    )
    __unimplemented_command_text_en = (
        "This command hasn't been implemented yet.😔😔\n"
        "Type /about_me to contact the developer."
    )
    __unexpected_error_text_en = (
        "Something went wrong...😢😢\n"
        "You can sent error report using the /report command. "
        "If you describe the issue and steps, how to reproduce it in the report, this can help to fix it faster."
    )
    __unexpected_error_with_report_text_en = (
        "Something went wrong...😢😢 \n"
        "But don't worry, I've sent the error report to my developer. I suppose, this issue will be fixed soon."
    )

    # ## UKRAINIAN LOCALIZATION ## #
    __no_rights_to_pin_message_text_ukr = (
        'Я не маю достатньо прав, щоб закріпити повідомлення.😢😒\n'
        'Будь ласка, надайте мені потрібні права, або попросіть закріпити повідомлення адміністратора чату👮‍♂️.'
    )
    __no_rights_to_unpin_message_text_ukr = (
        'Я б із зідоволенням відкріпив би потрібну чергу, але в мене недостатньо прав.😢😒\n'
        'Будь ласка, надайте мені потрібні права, або попросіть відкріпити повідомлення адміністратора чату👮‍♂️.'
    )
    __unknown_command_text_ukr = (
        'Невідома команда.😧\n'
        'Щоб отримати допомогу, введіть /help, або натисніть \'/\', щоб побачити список всіх команд та їхній опис.'
        'Оберіть потрібну команду та натисніть Tab, потім додайте необхідні аргументи та натисність Enter. \n'
        'Щоб ввімкнути підсказки, відправте команду /silent_mode, переконайтеся, що *режим тиші* _вимкнено_.'
    )
    __unimplemented_command_text_ukr = (
        'TODO: translation in progress...'
    )
    __unexpected_error_text_ukr = (
        'На жаль, щось пішло не так...😢😢\n'
        'Але Ви можете надіслати повідомлення про помилку, скориставшись командою /report.'
        'Якщо Ви опишете проблему та те, як її можна відтворити, це допоможе пришвидшити її вирішення.)'
    )
    __unexpected_error_with_report_text_ukr = (
        'На жаль, щось пішло не так...😢😢\n'
        'Але не переймайтеся, я вже відправив повідомлення про полку своєму розробнику.✉️ '
        'Думаю, скоро він зможе її виправити.'
    )

    def no_rights_to_pin_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__no_rights_to_pin_message_text_ukr
        else:
            text = self.__no_rights_to_pin_message_text_en
        return {'text': text}

    def no_rights_to_unpin_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__no_rights_to_unpin_message_text_ukr
        else:
            text = self.__no_rights_to_unpin_message_text_en
        return {'text': text}

    def unknown_command(self):
        text: str
        if self._lang == 'ukr':
            text = self.__unknown_command_text_ukr
        else:
            text = self.__unknown_command_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def unimplemented_command(self):
        text: str
        if self._lang == 'ukr':
            text = self.__unimplemented_command_text_ukr
        else:
            text = self.__unimplemented_command_text_en
        return {'text': text}

    def unexpected_error(self):
        text: str
        if self._lang == 'ukr':
            text = self.__unexpected_error_text_ukr
        else:
            text = self.__unexpected_error_text_en
        return {'text': text}

    def unexpected_error_with_report(self):
        text: str
        if self._lang == 'ukr':
            text = self.__unexpected_error_with_report_text_ukr
        else:
            text = self.__unexpected_error_with_report_text_en
        return {'text': text}
