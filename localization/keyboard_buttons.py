def get_cancel_button_text(lang: str = 'en') -> str:
    cancel_button: str
    if lang == 'en':
        cancel_button = 'Cancel❌'
    else:
        cancel_button = 'TODO'
    return cancel_button
