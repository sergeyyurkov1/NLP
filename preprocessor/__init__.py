import string


class Preprocessor:
    def remove_punctuation(self, text: str):
        trans = text.maketrans("", "", string.punctuation)

        return text.translate(trans)

    def remove_digits(self, text: str):
        trans = text.maketrans("", "", string.digits)

        return text.translate(trans)
