# TODO rename to CallbackButtonsText
class ButtonsText:
    _add_me_text_en = 'Enrol'
    _remove_me_text_en = 'Unenroll'
    _skip_me_text_en = 'Skip'
    _next_text_en = 'Next'
    _pin_queue = 'Pin queue'

    @staticmethod
    def add_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return ButtonsText._add_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def remove_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return ButtonsText._remove_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def skip_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return ButtonsText._skip_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def next_text(lang: str = 'en') -> str:
        if lang == 'en':
            return ButtonsText._next_text_en
        else:
            return 'TODO'

    @staticmethod
    def notify_text(lang: str = 'en') -> str:
        if lang == 'en':
            return ButtonsText._pin_queue
        else:
            return 'TODO'
