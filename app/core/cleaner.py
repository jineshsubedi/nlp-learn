import re


class TextCleaner:

    @staticmethod
    def remove_urls(text: str) -> str:
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    @staticmethod
    def remove_emails(text: str) -> str:
        return re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "",
            text
        )

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def clean(cls, text: str) -> str:

        text = cls.remove_urls(text)
        text = cls.remove_emails(text)
        text = cls.remove_extra_spaces(text)

        return text