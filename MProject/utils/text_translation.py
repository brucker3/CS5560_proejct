from googletrans import Translator


class TextTranslate:
    def __init__(self, language):
        self.language = language
        self.translator = Translator()

    def __call__(self, text):
        translation = self.translator.translate(text, dest=self.language)
        return translation.text
