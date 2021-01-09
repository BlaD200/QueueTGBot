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

from telegram import ParseMode


def private_unaccepted(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = (f'Add me to the group first.)\n\n'
                'Type /help for more information.')
    else:
        text = "TODO"
    return {'text': text}


def start_message_private(fullname: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = (f"Hello, {fullname}!\n"
                f"This bot helps you to create and manage queues in your group. Just add it to the group and type \n"
                f"/create_queue <queue name> \n"
                f"command.\n"
                f"\n"
                f"To see the help type /help\n"
                f"To the the detailed info about the bot type /about_me.")
    else:
        text = "TODO"
    return {'text': text}


def start_message_chat(fullname: str, user_id: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = (f"Hello, [{fullname}](tg://user?id={user_id})\! \n"
                "I've already here and waiting for your commands\.😉")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


def create_queue_exist(queue_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = f"Sorry, but the queue with the given name *{queue_name}* already exists."
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def create_queue_empty_name(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ('Queue name cannot be empty. '
                'To create a new queue type \n'
                '`/create_queue@queues_manager_bot <name>`.')
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def about_me_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = (
            "Having troubles with managing queues in your group? Want to make queues maximum honest and objective? "
            "Well, this is the decision!\n "
            "I'm QueueBot and I'll help you to do all stuff related to queues and managing them."
            "\n\n"
            "Just add me to the group and type \n"
            "/create_queue &lt;queue name&gt; \n"
            "command to create a queue. You can also type /notify_all command before creating any queue to notify "
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
            "Bot version: unreleased.\n"
            "Developer: @l3_l_a_cl\n"
            "Github repository: <a href='https://github.com/BlaD200/QueueTGBot'>link</a>\n")
    else:
        text = 'TODO'

    return {'text': text, 'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}


def help_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("Add this bot to the group and type\n"
                "/create_queue <queue name> \n"
                "command to create a queue. You can also type /notify_all command "
                "before creating any queue to notify group members when some queue was created. "
                "You can then add yourself to the created queue by typing\n"
                "/add_me <queue name> \n"
                "command. \n"
                "And, at the end, type \n"
                "/next <queue name> \n"
                "command to notify a group member, whose turn came and move the queue further.\n"
                "\n"
                "You can also type '/' to see all available commands.\n")
    else:
        text = "TODO"
    return {'text': text}


def help_message_in_chat(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'TODO'
    else:
        text = "TODO"
    return {'text': text}


def unknown_command(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("Unknown command. \n"
                "To see the help type /help or type '/' to see the hints for commands, "
                "press tab and complete selected command by adding required arguments.")
    else:
        text = "TODO"
    return {'text': text}


def unimplemented_command(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("This command hasn't been implemented yet.😔😔\n"
                "Type /about_me to contact the developer.")
    else:
        text = "TODO"
    return {'text': text}


def unexpected_error(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "Something went wrong...😢😢"
    else:
        text = "TODO"
    return {'text': text}
