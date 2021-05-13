# Copyright (C) 2021 Vladyslav Synytsyn
from os import getenv


BOT_VERSION = 'v1.0.1'

BOT_TOKEN = getenv('BOT_TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
ADMIN_ID = getenv('ADMIN_ID')

CACHE_TIME = 2

__all__ = [
    'BOT_TOKEN',
    'WEBHOOK_URL',
    'ADMIN_ID',
    'BOT_VERSION'
]
