from os import getenv


BOT_VERSION = 'unreleased'

BOT_TOKEN = getenv('BOT_TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
ADMIN_ID = getenv('ADMIN_ID')

__all__ = [
    'BOT_TOKEN',
    'WEBHOOK_URL',
    'ADMIN_ID',
    'BOT_VERSION'
]
