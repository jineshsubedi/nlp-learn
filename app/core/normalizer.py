import re
import unicodedata


class TextNormalizer:

    @staticmethod
    def normalize(text: str) -> str:

        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        # Unicode normalization
        text = unicodedata.normalize("NFC", text)

        # Remove leading and trailing whitespace
        text = text.strip()

        # Convert English characters to lowercase
        text = text.lower()

        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text)

        return text