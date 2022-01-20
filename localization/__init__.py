# Copyright (C) 2021 Vladyslav Synytsyn

from localization.info_and_help_strings import InfoAndHelpStrings
from localization.members_strings import MemberActionsStrings
from localization.queue_actions_strings import QueueActionsStrings
from localization.settings_strings import SettingsStrings
from localization.unwanted_behaviour_strings import UnwantedBehaviourStrings
from sql import create_session
from sql.domain import Chat


def get_queue_localization_for_chat(chat_id):
    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        return QueueActionsStrings(chat.language)
    return QueueActionsStrings('en')


def get_info_localization_for_chat(chat_id):
    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        return InfoAndHelpStrings(chat.language)
    return InfoAndHelpStrings('en')


def get_members_localization_for_chat(chat_id):
    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        return MemberActionsStrings(chat.language)
    return MemberActionsStrings('en')


def get_settings_localization_for_chat(chat_id):
    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        return SettingsStrings(chat.language)
    return SettingsStrings('en')


def get_error_localization_for_chat(chat_id):
    session = create_session()
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        return UnwantedBehaviourStrings(chat.language)
    return UnwantedBehaviourStrings('en')


__all__ = [
    'get_error_localization_for_chat',
    'get_settings_localization_for_chat',
    'get_members_localization_for_chat',
    'get_info_localization_for_chat',
    'get_queue_localization_for_chat',
    'InfoAndHelpStrings',
    'MemberActionsStrings',
    'QueueActionsStrings',
    'SettingsStrings',
    'UnwantedBehaviourStrings'
]
