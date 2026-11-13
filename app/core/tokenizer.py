import re
import unicodedata


class WordTokenizer:

    def tokenize(self, text: str) -> list[str]:

        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        text = unicodedata.normalize("NFC", text)

        # Match words (including Unicode letters, combining marks / diacritics
        # in Devanagari \u0900-\u097F excluding dandas \u0964\u0965),
        # contractions, and individual punctuation symbols.
        word_char = r"[^\W_\u0964\u0965]|[\u0900-\u0963\u0966-\u097F]"
        pattern = rf"(?:{word_char})+(?:['’](?:{word_char})+)*|[^\w\s\u0900-\u097F]|[\u0964\u0965]"

        tokens = re.findall(pattern, text, flags=re.UNICODE)

        return tokens

class SentenceTokenizer:
    """Robust sentence tokenizer supporting Nepali and English.

    Handles:
    - Nepali sentence enders (।, ॥) and standard enders (. ! ?)
    - Common Nepali and English honorifics / abbreviations (डा., प्रा., Dr., Mr., etc.)
    - Numbers with decimal points (e.g., 3.14)
    - Closing quotes or brackets following punctuation marks (e.g., 'हो।’')
    """

    DEFAULT_ABBREVIATIONS = {
        # Nepali abbreviations and honorifics
        "डा.", "प्रा.", "श्री.", "पं.", "मु.", "इ.", "वि.", "सं.",
        # English abbreviations and titles
        "dr.", "mr.", "mrs.", "ms.", "prof.", "sr.", "jr.",
        "etc.", "vs.", "e.g.", "i.e.", "st.", "approx.",
    }

    _SENTINEL = "\uE000"

    def __init__(self, custom_abbreviations: list[str] | set[str] | None = None):
        self.abbreviations = set(self.DEFAULT_ABBREVIATIONS)
        if custom_abbreviations:
            self.abbreviations.update(abbr.strip().lower() for abbr in custom_abbreviations)

    def _protect_patterns(self, text: str) -> str:
        # Protect decimal numbers (e.g. 3.14 -> 3\uE00014)
        text = re.sub(r"(\d+)\.(\d+)", rf"\g<1>{self._SENTINEL}\g<2>", text)

        # Protect known abbreviations (both single-dot like 'डा.' and multi-dot like 'का.म.पा.' or 'u.s.a.')
        def replace_abbr(match: re.Match) -> str:
            word = match.group(0)
            if word.lower() in self.abbreviations:
                return word.replace(".", self._SENTINEL)
            return word

        text = re.sub(r"(?:[\w\u0900-\u097F]+\.)+", replace_abbr, text, flags=re.UNICODE)
        return text

    def tokenize(self, text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        text = unicodedata.normalize("NFC", text.strip())
        if not text:
            return []

        # Protect non-sentence periods (abbreviations, numbers)
        protected = self._protect_patterns(text)

        # Match terminal punctuation followed by optional closing quotation / brackets, then whitespace
        boundary_pattern = r"([.!?।॥]['\"’”\)\]]*)\s+"
        marked = re.sub(boundary_pattern, r"\1\n", protected)

        sentences = marked.split("\n")

        # Restore protected dots and clean whitespace
        return [
            s.replace(self._SENTINEL, ".").strip()
            for s in sentences
            if s.strip()
        ]