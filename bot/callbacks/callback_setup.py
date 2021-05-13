from telegram.ext import Dispatcher, CallbackQueryHandler

from bot.callbacks.callback_data_actions import ADD_ME, REMOVE_ME, SKIP_ME, NEXT, NOTIFY, ENG_LANGUAGE, URK_LANGUAGE
from bot.callbacks.callback_handlers import add_me_callback, remove_me_callback, skip_me_callback, next_callback, \
    pin_queue_callback, language_setup_for_chat_callback


def setup_callbacks(dispatcher: Dispatcher):
    # Registering callback handlers here
    dispatcher.add_handler(CallbackQueryHandler(add_me_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{ADD_ME}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(remove_me_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{REMOVE_ME}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(skip_me_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{SKIP_ME}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(next_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{NEXT}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(pin_queue_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{NOTIFY}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(language_setup_for_chat_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{ENG_LANGUAGE}).*$'))

    dispatcher.add_handler(CallbackQueryHandler(language_setup_for_chat_callback,
                                                pattern=rf'^.*([\'"]action[\'"]:\s*{URK_LANGUAGE}).*$'))
