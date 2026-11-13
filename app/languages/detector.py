import re


class LanguageDetector:

    _NEPALI_WORD_PATTERN = re.compile(r"[\u0900-\u0963\u0966-\u097F]+")
    _ENGLISH_WORD_PATTERN = re.compile(r"[A-Za-z]+")

    @classmethod
    def detect(cls, text: str, mixed_threshold: float = 0.3) -> str:
        """Detect language using word-level counts.

        - If both languages exceed `mixed_threshold` of total valid words, returns 'mixed'.
        - Otherwise returns the dominant language ('ne' or 'en').
        - Returns 'unknown' if no words in either script are found.
        """
        words = text.split()

        nepali_words = 0
        english_words = 0

        for word in words:
            has_nepali = bool(cls._NEPALI_WORD_PATTERN.search(word))
            has_english = bool(cls._ENGLISH_WORD_PATTERN.search(word))

            if has_nepali and has_english:
                nepali_words += 0.5
                english_words += 0.5
            elif has_nepali:
                nepali_words += 1
            elif has_english:
                english_words += 1

        total_words = nepali_words + english_words
        if total_words == 0:
            return "unknown"

        nepali_ratio = nepali_words / total_words
        english_ratio = english_words / total_words

        # If both languages have significant presence, classify as mixed
        if nepali_ratio >= mixed_threshold and english_ratio >= mixed_threshold:
            return "mixed"

        if nepali_words > english_words:
            return "ne"

        return "en"
