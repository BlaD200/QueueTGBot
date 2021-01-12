from os import getenv


BOT_TOKEN = getenv('BOT_TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
ADMIN_ID = getenv('ADMIN_ID')
BOT_VERSION = getenv('BOT_VERSION')

__all__ = [
    'BOT_TOKEN',
    'WEBHOOK_URL',
    'ADMIN_ID',
    'BOT_VERSION'
]
