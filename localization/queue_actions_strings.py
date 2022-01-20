# Copyright (C) 2021 Vladyslav Synytsyn
# noinspection PyUnresolvedReferences
"""
In this module defines all text constants used by the bot to create text replies.

All functions returns :class:`dict`, that contains arguments, needed to display message correctly,
like ``parse_mode`` or ``disable_web_page_preview``.

Examples:
    >>> bot.send_message(**create_queue_exist(queue_name='name', lang='en'))

See Also:
    :class:`telegram.bot.Bot`
"""
from typing import List

from telegram import ParseMode
from telegram.utils.helpers import escape_markdown

from app_logging import get_logger
from localization.base_localization import BaseLocalization


logger = get_logger(__name__)


class QueueActionsStrings(BaseLocalization):
    # ## ENGLISH LOCALIZATION ## #
    __create_queue_empty_name_text_en = (
        'Queue name cannot be empty. To create a new queue, type \n'
        '/create_queue <name>.'
    )
    __create_queue_exist_text_en_f = "Sorry, but the queue with the given name *{queue_name}* already exists\."
    "format options: `queue_name`"
    __create_queue_unsupported_name_text_en_f = (
        'You tried to create queue with some of the reserved characters\. '
        'Try not to use any of them: *{reserved_characters}* or '
        'try not to use forward slash "\\\\" before any of them\.'
    )
    "format options: `reserved_characters`"
    __queue_not_exist_text_en_f = "Sorry, but the queue with the given name *{queue_name}* doesn't exist."
    "format options: `queue_name`"
    __show_queues__message_text_en_f = "Active Queues:\n\n{queue_names}"
    "format options: queue_names"
    __show_queue_members_text_en_f = 'Members: \n{members}'
    "format options: members"
    __command_empty_queue_name_text_en_f = (
        "You must specify a queue name or reply to the message with the queue.\n"
        "Usage: \n/{command_name} <name>"
    )
    "format options: `command_name`"
    __callback_empty_queue_id_text_en_f = (
        "Something went wrong😔🤭. Try to use /{command_name} <queue>"
    )
    "format options: `command_name"

    __deleted_queue__message_text_en = "The queue was deleted.☑️"
    __delete_queue_empty_name_text_en = (
        'Queue name cannot be empty. To delete the queue, type \n'
        '/delete_queue <name>.'
    )
    __no_queues_message__text_en = (
        "There no queues in this chat created yet🤷‍♂️.\n\n"
        "To create a queue, type\n"
        "/create_queue <name>"
    )
    __show_queue_members_empty_text_en = 'No members here yet\.'
    __reply_to_wrong_queue_members_message__text_eng = (
        'You must reply to the message, contains queue members, to make the command works without arguments.\n'
        '_Note_: the queue must be active (not deleted).'
    )
    __enter_queue_name__message_text_en = 'Enter the name of the queue:'
    __cancel_queue_creation__message_text_en = 'Okay, the queue creation was cancelled.☑️'
    __cancel_queue_deletion__message_text_en = 'Okay, the queue deletion was cancelled.☑️'
    __callback_empty_queue_id__for_pin_text_en = (
        "Something went wrong with with this button. "
        "Pin message manually, please, or use "
        "type /notify_all and create a new queue."
    )
    __already_in_the_queue_text_en = "You are already in this queue."
    __not_in_the_queue_yet_text_en = "You haven't been registered in this queue yet."
    __next_reached_queue_end__text_en = "The queue has reached the end."

    # ## UKRAINIAN LOCALIZATION ## #
    __create_queue_exist_text_ukr = 'Вибачте, але черга з вказаною назвою *{queue_name}* вже існує\.'
    __create_queue_empty_name_text_ukr = 'TODO: translation in progress...'
    "format options: `queue_name`"
    __create_queue_unsupported_name_text_ukr = (
        'Ім\'я, яке Ви ввели містить символи, які не підтримуються\. '
        'Спробуйте не використовувати жоден з них: *{reserved_characters}* або '
        'спробуйте поставити слеш "\\\\" перед усіма зарезервованими символами\.'
    )
    "format options: ``reserved_characters``"
    __queue_not_exist_text_ukr_f = "Вибачте, але черги з вказаною назвою *{queue_name}* не існує."
    "format options: `queue_name`"
    __show_queues__message_text_ukr_f = "Активні черги:\n\n{queue_names}"
    "format options: queue_names"
    __show_queue_members_text_ukr_f = 'Учасники: \n{members}'
    "format options: members"
    __command_empty_queue_name_text_ukr_f = (
        "Ви маєте вказати ім'я черги, або відповісти на повідомлення з учасниками черги.\n"
        "Використання: \n/{command_name} <ім'я>"
    )
    __callback_empty_queue_id_text_ukr_f = (
        "Щось пішло не так😔🤭. Спробуйте використати /{command_name} <черга>"
    )
    "format options: `command_name"

    __deleted_queue__message_text_ukr = 'Черга видалена.☑️'
    __delete_queue_empty_name_text_ukr = 'TODO: translation in progress...'
    __no_queues_message__text_ukr = (
        "В цьому чаті ще немає створених черг🤷‍♂️.\n\n"
        "Щоб створити чергу, введіть \n"
        "/create_queue <name>."
    )
    __show_queue_members_empty_text_ukr = 'В цій черзі ще немає учасників\.'
    __reply_to_wrong_queue_members_message__text_ukr = (
        'Ви маєте відповісти на повідомлення, яке містить учасників черги, щоб команда спрацювала без аргументів.\n'
        '_Зверніть увагу_: черга має бути активною (не видаленою).'
    )
    __enter_queue_name__message_text_ukr = 'Введіть назву черги:'
    __cancel_queue_creation__message_text_ukr = 'Гаразд, створення черги скасовано.☑️'
    __cancel_queue_deletion__message_text_ukr = 'Гаразд, видалення черги скасовано.☑️'
    __callback_empty_queue_id__for_pin_text_ukr = (
        "Щось пішло не так😔🤭. "
        "Будь ласка, закріпіть повідомлення власноруч, або введіть /notify_all, і створіть нову чергу."
    )
    __already_in_the_queue_text_ukr = 'Ви вже й так у цій черзі😉.'
    __not_in_the_queue_yet_text_ukr = 'Ви ще не реєструвалися у цій черзі🤷‍♂️.'
    __next_reached_queue_end__text_ukr = 'Черга добігла кінця🙂.'

    def create_queue_exist(self, queue_name: str):
        text: str
        if self._lang == 'ukr':
            text = self.__create_queue_exist_text_ukr.format(queue_name=escape_markdown(queue_name, 2))
        else:
            text = self.__create_queue_exist_text_en_f.format(queue_name=escape_markdown(queue_name, 2))
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def create_queue_empty_name(self):
        text: str
        if self._lang == 'ukr':
            text = self.__create_queue_empty_name_text_ukr
        else:
            text = self.__create_queue_empty_name_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def create_queue_unsupported_name(self):
        text: str
        if self._lang == 'ukr':
            text = self.__create_queue_unsupported_name_text_ukr.format(
                reserved_characters=escape_markdown("_*[]()~`>#+-=|{}.!", 2)
            )
        else:
            text = self.__create_queue_unsupported_name_text_en_f.format(
                reserved_characters=escape_markdown("_*[]()~`>#+-=|{}.!", 2)
            )
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def delete_queue_empty_name(self):
        text: str
        if self._lang == 'ukr':
            text = self.__delete_queue_empty_name_text_ukr
        else:
            text = self.__delete_queue_empty_name_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def queue_not_exist(self, queue_name: str):
        text: str
        if self._lang == 'ukr':
            text = self.__queue_not_exist_text_ukr_f.format(queue_name=queue_name)
        else:
            text = self.__queue_not_exist_text_en_f.format(queue_name=queue_name)
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def deleted_queue_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__deleted_queue__message_text_ukr
        else:
            text = self.__deleted_queue__message_text_en
        return {'text': text}

    def show_queues_message(self, queues: List[str]):
        queue_names_formatted_list = [f'• *{queue_name}*\n' for queue_name in queues]
        text: str
        if self._lang == 'ukr':
            text = self.__show_queues__message_text_ukr_f.format(queue_names=''.join(queue_names_formatted_list))
        else:
            text = self.__show_queues__message_text_en_f.format(queue_names=''.join(queue_names_formatted_list))
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def show_queue_members(self, queue_name: str, members: List[str] = None, current_member: int = 0):
        text: str
        if not members:
            members = []
        members_names = ''.join(
            [f'{i}\. '
             f'{(lambda member: member if i != current_member else f"*{member}*")(escape_markdown(member_name, 2))}'
             f'\n'
             for (i, member_name) in enumerate(members)])

        if self._lang == 'ukr':
            if not members:
                queue_members_formatted = self.__show_queue_members_empty_text_ukr
            else:
                queue_members_formatted = self.__show_queue_members_text_ukr_f.format(members=members_names)
        else:
            if not members:
                queue_members_formatted = self.__show_queue_members_empty_text_en
            else:
                queue_members_formatted = self.__show_queue_members_text_en_f.format(members=members_names)

        queue_name_escaped = escape_markdown(queue_name, 2)
        text = (f"*{queue_name_escaped}*\n\n"
                f"{queue_members_formatted}")

        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def reply_to_wrong_queue_members_message__message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__reply_to_wrong_queue_members_message__text_ukr
        else:
            text = self.__reply_to_wrong_queue_members_message__text_eng
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def show_no_queues_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__no_queues_message__text_ukr
        else:
            text = self.__no_queues_message__text_en
        return {'text': text}

    def command_empty_queue_name(self, command_name: str):
        text: str
        if self._lang == 'ukr':
            text = self.__command_empty_queue_name_text_ukr_f.format(command_name=command_name)
        else:
            text = self.__command_empty_queue_name_text_en_f.format(command_name=command_name)
        return {'text': text}

    def enter_queue_name_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__enter_queue_name__message_text_ukr
        else:
            text = self.__enter_queue_name__message_text_en
        return {'text': text}

    def cancel_queue_creation_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__cancel_queue_creation__message_text_ukr
        else:
            text = self.__cancel_queue_creation__message_text_en
        return {'text': text}

    def cancel_queue_deletion_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__cancel_queue_deletion__message_text_ukr
        else:
            text = self.__cancel_queue_deletion__message_text_en
        return {'text': text}

    def callback_empty_queue_id(self, command_name: str, lang: str = None):
        text: str
        lang = self._lang if not lang else lang
        if lang == 'ukr':
            text = self.__callback_empty_queue_id_text_ukr_f.format(command_name=command_name)
        else:
            text = self.__callback_empty_queue_id_text_en_f.format(command_name=command_name)
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def callback_empty_queue_id__for_pin(self, *args, lang: str = None):
        text: str
        lang = self._lang if not lang else lang
        if lang == 'ukr':
            text = self.__callback_empty_queue_id__for_pin_text_ukr
        else:
            text = self.__callback_empty_queue_id__for_pin_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def already_in_the_queue(self):
        text: str
        if self._lang == 'ukr':
            text = self.__already_in_the_queue_text_ukr
        else:
            text = self.__already_in_the_queue_text_en
        return {'text': text}

    def not_in_the_queue_yet(self):
        text: str
        if self._lang == 'ukr':
            text = self.__not_in_the_queue_yet_text_ukr
        else:
            text = self.__not_in_the_queue_yet_text_en
        return {'text': text}

    def next_reached_queue_end(self):
        text: str
        if self._lang == 'ukr':
            text = self.__next_reached_queue_end__text_ukr
        else:
            text = self.__next_reached_queue_end__text_en
        return {'text': text}
