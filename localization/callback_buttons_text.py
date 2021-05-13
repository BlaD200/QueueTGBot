class QueueMemberCallbackButtonsText:
    _add_me_text_en = 'Enrol'
    _remove_me_text_en = 'Unenroll'
    _skip_me_text_en = 'Skip'
    _next_text_en = 'Next'
    _pin_queue = 'Pin queue'

    @staticmethod
    def add_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return QueueMemberCallbackButtonsText._add_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def remove_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return QueueMemberCallbackButtonsText._remove_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def skip_me_text(lang: str = 'en') -> str:
        if lang == 'en':
            return QueueMemberCallbackButtonsText._skip_me_text_en
        else:
            return 'TODO'

    @staticmethod
    def next_text(lang: str = 'en') -> str:
        if lang == 'en':
            return QueueMemberCallbackButtonsText._next_text_en
        else:
            return 'TODO'

    @staticmethod
    def notify_text(lang: str = 'en') -> str:
        if lang == 'en':
            return QueueMemberCallbackButtonsText._pin_queue
        else:
            return 'TODO'


class SelectLanguageCallbackButtonsText:
    _en_language = 'English🇬🇧'
    _urk_language = 'Українська🇺🇦'

    @staticmethod
    def english_language_text() -> str:
        return SelectLanguageCallbackButtonsText._en_language

    @staticmethod
    def ukrainian_language_text() -> str:
        return SelectLanguageCallbackButtonsText._urk_language
