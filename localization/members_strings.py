from telegram import ParseMode
from telegram.utils.helpers import escape_markdown

from localization.base_localization import BaseLocalization


class MemberActionsStrings(BaseLocalization):
    # ## ENGLISH LOCALIZATION ## #
    __next_member_notify_message_en_f = (
        "[{fullname_capital}](tg://user?id={user_id}), "
        "your turn has come in the queue *{queue_name_escaped}*\!"
    )
    "format options: ``fullname_capital``, ``user_id``, ``queue_name_escaped``"
    __cancel_notify_next_message_text_en = 'Okay, no one will be notified.'
    __cannot_skip_message_text_en = (
        "You are alone or the last one in this queue, so, command has no sense..."
    )

    # ## UKRAINIAN LOCALIZATION ## #
    __next_member_notify_message_ukr_f = (
        "[{fullname_capital}](tg://user?id={user_id}), "
        "настал твоя черга в *{queue_name_escaped}*\!"
    )
    "format options: ``fullname_capital``, ``user_id``, ``queue_name_escaped``"
    __cancel_notify_next_message_text_ukr = 'Гаразд, сповістимо наступного разу.'
    __cannot_skip_message_text_ukr = 'Ти один або останній у черзі, тому в команді немає сенсу...'

    def cancel_notify_next_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__cancel_notify_next_message_text_ukr
        else:
            text = self.__cancel_notify_next_message_text_en
        return {'text': text}

    def cannot_skip(self):
        text: str
        if self._lang == 'ukr':
            text = self.__cannot_skip_message_text_ukr
        else:
            text = self.__cannot_skip_message_text_en
        return {'text': text}

    def next_member_notify(self, fullname: str, user_id: int, queue_name: str):
        text: str
        if self._lang == 'ukr':
            text = self.__next_member_notify_message_ukr_f
        else:
            text = self.__next_member_notify_message_en_f
        text = text.format(fullname_capital=fullname.capitalize(), user_id=user_id,
                           queue_name_escaped=escape_markdown(queue_name, 2))
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}
