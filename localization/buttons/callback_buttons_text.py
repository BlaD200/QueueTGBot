class QueueMemberCallbackButtonsText:
    _add_me_text_en = 'Enrol'
    _remove_me_text_en = 'Unenroll'
    _skip_me_text_en = 'Skip me'
    _move_to_end_text_en = 'Go to the end'
    _next_text_en = 'Next'
    _pin_queue_en = 'Pin queue'

    _add_me_text_ukr = 'Записатися'
    _remove_me_text_ukr = 'Виписатися'
    _skip_me_text_ukr = 'Пропустити чергу'
    _move_to_end_text_ukr = 'В кінець черги'
    _next_text_ukr = 'Наступний'
    _pin_queue_ukr = 'Закріпити чергу'

    def __init__(self, language):
        """

        Args:
            language: The language, the text will be displayed in
        """
        self._lang = language

    def add_me_text(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._add_me_text_en
        else:
            return QueueMemberCallbackButtonsText._add_me_text_ukr

    def remove_me_text(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._remove_me_text_en
        else:
            return QueueMemberCallbackButtonsText._remove_me_text_ukr

    def skip_me_text(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._skip_me_text_en
        else:
            return QueueMemberCallbackButtonsText._skip_me_text_ukr

    def move_me_to_the_end(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._move_to_end_text_en
        else:
            return QueueMemberCallbackButtonsText._move_to_end_text_ukr

    def next_text(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._next_text_en
        else:
            return QueueMemberCallbackButtonsText._next_text_ukr

    def notify_text(self) -> str:
        if self._lang == 'en':
            return QueueMemberCallbackButtonsText._pin_queue_en
        else:
            return QueueMemberCallbackButtonsText._pin_queue_ukr


class SelectLanguageCallbackButtonsText:
    _en_language = 'English🇬🇧'
    _urk_language = 'Українська🇺🇦'

    @staticmethod
    def english_language_text() -> str:
        return SelectLanguageCallbackButtonsText._en_language

    @staticmethod
    def ukrainian_language_text() -> str:
        return SelectLanguageCallbackButtonsText._urk_language
