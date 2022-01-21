from typing import List


class CancelKeyboardButtonText:
    _cancel_button_eng = 'Cancel❌'
    _cancel_button_ukr = 'Відмінити❌'

    def __init__(self, language: str):
        """

        Args:
            language: The language, the text will be displayed in
        """
        self._lang = language

    def get_cancel_button_text(self) -> str:
        cancel_button: str
        if self._lang == 'en':
            cancel_button = self._cancel_button_eng
        else:
            cancel_button = self._cancel_button_ukr
        return cancel_button

    @staticmethod
    def get_all_cancel_texts() -> List[str]:
        return [
            CancelKeyboardButtonText._cancel_button_eng,
            CancelKeyboardButtonText._cancel_button_ukr
        ]
