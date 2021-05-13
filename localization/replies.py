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


logger = get_logger(__name__)


def chat_language_setting(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "👍Okay, now I'll speak *English*🇬🇧 in this chat\. Good luck😉"
    else:
        text = "👍Добре, тепер я буду використовувати *Українську*🇺🇦 у цьому чаті\. Насолоджуйтеся😉"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


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
        text = (f'Hello, [{fullname}](tg://user?id={user_id})\! \n'
                'I\'ve already here and waiting for your commands\.😉\n\n'
                'If you are a little bit perplexed, don\'t worry, type /help to get the short instruction\.🤗😌')
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


def create_queue_exist(queue_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = f"Sorry, but the queue with the given name *{escape_markdown(queue_name, 2)}* already exists\."
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


def create_queue_empty_name(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ('Queue name cannot be empty. '
                'To create a new queue, type \n'
                '`/create_queue <name>`.')
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def no_rights_to_pin_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "I have no rights to pin this message.😢😒\n" \
               "Give me this permission or ask your admin to pin manually."
    else:
        text = "TODO"
    return {'text': text}


def no_rights_to_unpin_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "I would unpin that queue with pleasure, but you didn't give me the necessary rights.😢😒\n" \
               "Give me this permission or ask your admin to unpin manually."
    else:
        text = "TODO"
    return {'text': text}


def delete_queue_empty_name(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ('Queue name cannot be empty. '
                'To delete the queue, type \n'
                '`/delete_queue <name>`.')
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def queue_not_exist(queue_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = f"Sorry, but the queue with the given name *{queue_name}* doesn't exist."
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def deleted_queue_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "The queue was deleted."
    else:
        text = "TODO"
    return {'text': text}


def show_queues_message(queues: List[str], lang: str = 'en'):
    queue_names_formatted_list = [f'• *{queue_name}*\n' for queue_name in queues]
    text: str
    if lang == 'en':
        text = ("Active Queues:\n\n"
                f"{''.join(queue_names_formatted_list)}")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def show_queue_members(queue_name: str, members: List[str] = None, current_member: int = 0, lang: str = 'en'):
    text: str
    if lang == 'en':
        if not members:
            queue_members_formatted = 'No members here yet\.'
        else:
            queue_members_formatted = "Members:\n" + (
                ''.join(
                    [f'{i}\. '
                     f'{(lambda member: member if i != current_member else f"*{member}*")(escape_markdown(member_name, 2))}'
                     f'\n'
                     for (i, member_name) in enumerate(members)]))
        queue_name_escaped = escape_markdown(queue_name, 2)
        text = (f"*{queue_name_escaped}*\n\n"
                f"{queue_members_formatted}")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


def cancel_notify_next_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Okay, no one will be notified.'
    else:
        text = "TODO"
    return {'text': text}


def show_queues_message_empty(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("There no queues in this chat created yet.\n\n"
                "To create a queue, type\n"
                "`/create_queue <name>`")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def command_empty_queue_name(command_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("You must specify a queue name or reply to the message with the queue.\n"
                f"Usage: `/{command_name} <name>`")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def enter_queue_name_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Enter the name of the queue:'
    else:
        text = "TODO"
    return {'text': text}


def queue_created_remove_keyboard_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = '✅'
    else:
        text = "✅"
    return {'text': text}


def cancel_queue_creation_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Okay, the queue creation was cancelled.'
    else:
        text = "TODO"
    return {'text': text}


def cancel_queue_deletion_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Okay, the queue deletion was cancelled.'
    else:
        text = "TODO"
    return {'text': text}


def callback_empty_queue_id(command_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("Something went wrong with with this button. Try to use command instead.\n"
                f"Usage: `/{command_name} <name>`")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def callback_empty_queue_id__for_pin(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("Something went wrong with with this button. Pin message manually, please, or use "
                "type `/notify_all` and create a new queue.")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def already_in_the_queue(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "You are already in this queue."
    else:
        text = "TODO"
    return {'text': text}


def not_in_the_queue_yet(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "You haven't been registered in this queue yet."
    else:
        text = "TODO"
    return {'text': text}


def cannot_skip(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "You are alone or the last one in this queue, so, there no sense in the skip command..."
    else:
        text = "TODO"
    return {'text': text}


def next_reached_queue_end(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "The queue has reached the end."
    else:
        text = "TODO"
    return {'text': text}


def next_member_notify(fullname: str, user_id: int, queue_name: str, lang: str = 'en'):
    text: str
    if lang == 'en':
        text = f"[{fullname.capitalize()}](tg://user?id={user_id}), " \
               f"your turn has come in the queue *{queue_name}*\!"
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN_V2}


def reply_to_wrong_message_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'You must reply to the message, contains queue members, to make the command works without arguments.\n' \
               '_Note_: the queue must be active (not deleted).'
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def notify_all_disabled_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'The messages with new queues *will not* be pinned more.\n\n' \
               '_And members in this chat will not be notified when a new queue will be created..._'
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def notify_all_enabled_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'The messages with new queues *will be* pinned!\n\n'
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def select_language_message(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = 'Please, select the language, in which the bot will speak'
    else:
        text = "TODO"
    return {'text': text}


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
            "Bot version: unreleased.\n"
            "Developer: @l3_l_a_cl\n"
            "Github repository: <a href='https://github.com/BlaD200/QueueTGBot'>link</a>\n")
    else:
        text = 'TODO'

    return {'text': text, 'parse_mode': ParseMode.HTML, 'disable_web_page_preview': True}


def help_message_private(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ("Add this bot to the group and type\n"
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
                "You can also type '/' to see all available commands.\n")
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


def help_message_in_chat(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = ('Alright, I\'ve already in the group.🥳\n'
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
                'So simple, yes?) Well, good luck, _and let there be only honest queues._😎😎')
    else:
        text = "TODO"
    return {'text': text, 'parse_mode': ParseMode.MARKDOWN}


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
        text = "Something went wrong...😢😢\n" \
               "You can sent error report using the /report command. " \
               "If you describe the issue and steps, how to reproduce it in the report, this can help to fix it faster."
    else:
        text = "TODO"
    return {'text': text}


def unexpected_error_with_report(lang: str = 'en'):
    text: str
    if lang == 'en':
        text = "Something went wrong...😢😢 \n" \
               "But don't worry, I've sent the error report to my developer. I suppose, this issue will be fixed soon."
    else:
        text = "TODO"
    return {'text': text}
