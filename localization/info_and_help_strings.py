from telegram import ParseMode

from bot.constants import BOT_VERSION
from localization.base_localization import BaseLocalization


def remove_keyboard_message():
    text = '✅'
    return {'text': text}


class InfoAndHelpStrings(BaseLocalization):
    # ## ENGLISH LOCALIZATION ## #
    __start_message_private_text_en_f = (
        "Hello, {fullname}!\n"
        "This bot helps you to create and manage queues in your group. \n"
        "Just add it to the group and type \n"
        "/create_queue <queue name> \n"
        "command."
        "\n"
        "To see the help type /help \n"
        "To see the detailed info about the bot type /about_me."
    )
    "formatting options: ``fullname``"
    __start_message_chat_text_en_f = (
        "Hello, [{fullname}](tg://user?id={user_id})\\! \n"
        "I\\'ve already here and waiting for your commands\\.😉\n\n"
        "If you are a little bit perplexed, don\\'t worry, type /help to get the short instruction\\.🤗😌"
    )
    "formatting options: ``fullname``, ``user_id``"
    __private_unaccepted_message_text_en = 'Add me to the group first.)\n\nType /help for more information.'

    __about_me_message_text_en_f = (
        "Having troubles with managing queues in your group? Want to make queues maximum honest and objective? "
        "Well, this is the decision!\n "
        "I'm QueueBot and I'll help you to do all stuff related to queues and managing them."
        "\n\n"
        "Just add me to the group and type \n"
        "/create_queue &lt;queue name&gt; \n"
        "command to create a queue. You can also type give me the rights to pin the messages"
        " before creating any queue to notify "
        "group members when some queue was created. This will help them to be in touch and don't miss the new "
        "queues, they could want to participate in.\n "
        "You can then add yourself to the created queue by typing\n"
        "/add_me &lt;queue name&gt; \n"
        "command. \n"
        "And, at the end, type \n"
        "/next &lt;queue name&gt; \n"
        "command to notify a group member, whose turn came and move the queue further.\n"
        "\n"
        "My creator said that he will be very thankful for your feedback, any suggestions are welcomed and bug "
        "reports are priceless!\n "
        "\n"
        "Bot version: {BOT_VERSION}.\n"
        "Developer: @l3_l_a_cl\n"
        "Github repository: <a href='https://github.com/BlaD200/QueueTGBot'>link</a>\n"
    )
    "formatting options: ``BOT_VERSION``"
    __help_message_private_text_en = (
        "Add this bot to the group and type\n"
        "/create\_queue <queue name> \n"
        "command to create a queue. You _should_ also give this bot the rights to *pin* the messages "
        "before creating any queue to notify group members when some queue was created. "
        "You can then add yourself to the created queue by typing\n"
        "/add\_me <queue name> \n"
        "command. \n"
        "And, in the end, type \n"
        "/next <queue name> \n"
        "command to notify a group member, whose turn came and move the queue further.\n"
        "For your comfort, you can reply with command add\_me, remove\_me, skip\_me, next, and show\_members to "
        "the message with queue and don't type the name by hand.)☺\n"
        "\n"
        "You can also type '/' to see all available commands.\n"
    )
    __help_message_chat_text_en = (
        'Alright, I\'ve already in the group.🥳\n'
        'Now, give me the rights to *pin* the messages, so your group members will be *notified* '
        'when the queue will be created!'
        '\n\n'
        'Done? Amazing!) To create a new queue send \n'
        '/create\_queue <queue name> \n'
        'command. And don\'t forget to type the future queue\'s *name*.)👍 '
        '\n\n'
        'Next step is to become the *participant* in the created queue.✅ '
        'To do this, just reply to the message, with the corresponding queue, '
        'with the /add\_me command. (You can also leave the queue by sending /remove\_me command) '
        '\n\n'
        'And the last important thing: when the time comes, to move your queue further, '
        'just reply to the queue with the /next command, and the next member will be notified, '
        'so no one will skip their turn!💪'
        '\n\n'
        'So simple, yes?) Well, good luck, _and let there be only honest queues._😎😎'
    )

    # ## UKRAINIAN LOCALIZATION ## #
    __start_message_private_text_ukr_f = 'TODO: translation in progress...'
    "formatting options: ``fullname``"
    __start_message_chat_text_ukr_f = 'TODO: translation in progress...'
    "formatting options: ``fullname``, ``user_id``"
    __private_unaccepted_message_text_ukr = (
        'Для початку, додайте мене до групи.)\n\n'
        'Скористайтеся командою /help для детальнішої інформації.'
    )

    __about_me_message_text_ukr_f = 'TODO: translation in progress...'
    "formatting options: ``BOT_VERSION``"
    __help_message_private_text_ukr = 'TODO: translation in progress...'
    __help_message_chat_text_ukr = 'TODO: translation in progress...'

    def start_message_private(self, fullname: str):
        if self._lang == 'ukr':
            text = self.__start_message_private_text_ukr_f
        else:
            text = self.__start_message_private_text_en_f
        text = text.format(fullname=fullname)
        return {'text': text}

    def start_message_chat(self, fullname: str, user_id: str):
        if self._lang == 'ukr':
            text = self.__start_message_chat_text_ukr_f
        else:
            text = self.__start_message_chat_text_en_f
        text = text.format(fullname=fullname, user_id=user_id)
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}

    def private_unaccepted_message(self):
        if self._lang == 'ukr':
            text = self.__private_unaccepted_message_text_ukr
        else:
            text = self.__private_unaccepted_message_text_en
        return {'text': text}

    def about_me_message(self):
        text: str
        if self._lang == 'ukr':
            text = self.__about_me_message_text_ukr_f
        else:
            text = self.__about_me_message_text_en_f
        text = text.format(BOT_VERSION=BOT_VERSION)
        return {'text': text, 'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}

    def help_message_private(self):
        text: str
        if self._lang == 'ukr':
            text = self.__help_message_private_text_ukr
        else:
            text = self.__help_message_private_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}

    def help_message_in_chat(self):
        text: str
        if self._lang == 'ukr':
            text = self.__help_message_chat_text_ukr
        else:
            text = self.__help_message_chat_text_en
        return {'text': text, 'parse_mode': ParseMode.MARKDOWN}
