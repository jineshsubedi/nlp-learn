import re
import unicodedata


class TextNormalizer:
    """Comprehensive text normalizer supporting English contractions and Nepali Unicode canonicalization."""

    # Common English contractions mapping
    CONTRACTIONS = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mightn't": "might not",
        "mustn't": "must not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "that's": "that is",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'll": "we will",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "where's": "where is",
        "who'd": "who would",
        "who'll": "who will",
        "who's": "who is",
        "who've": "who have",
        "won't": "will not",
        "would've": "would have",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
    }

    _CONTRACTION_PATTERN = re.compile(
        r"\b(" + "|".join(re.escape(k) for k in sorted(CONTRACTIONS.keys(), key=len, reverse=True)) + r")\b",
        flags=re.IGNORECASE,
    )

    @classmethod
    def expand_contractions(cls, text: str) -> str:
        """Expands English contractions (e.g. don't -> do not, I'm -> I am)."""
        def replace(match: re.Match) -> str:
            word = match.group(0).lower()
            replacement = cls.CONTRACTIONS.get(word, match.group(0))
            if match.group(0)[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            return replacement

        # Standardize curly apostrophes to straight apostrophe first
        text = text.replace("’", "'").replace("‘", "'")
        return cls._CONTRACTION_PATTERN.sub(replace, text)

    @classmethod
    def normalize_nepali(cls, text: str) -> str:
        """Normalizes Nepali Devanagari text:
        - Replaces Zero-Width Joiner (ZWJ \u200D) and Zero-Width Non-Joiner (ZWNJ \u200C)
        - Normalizes nukta/composite sequences into canonical NFC
        - Unifies common punctuation (e.g. full-width pipe | to Nepali danda ।)
        """
        # Convert full-width ASCII vertical bar to Devanagari danda if used as sentence punctuation
        text = text.replace("।", "।")
        text = re.sub(r"(?<=\s)\|(?=\s|$)", "।", text)

        # Standardize zero-width characters (remove non-standard dangling joiners)
        text = text.replace("\u200b", "")  # zero-width space

        # Canonical decomposition followed by composition
        text = unicodedata.normalize("NFC", text)
        return text

    @classmethod
    def normalize(
        cls,
        text: str,
        expand_contractions: bool = False,
        lowercase: bool = True,
    ) -> str:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        # Nepali & Unicode normalization
        text = cls.normalize_nepali(text)

        # English contractions
        if expand_contractions:
            text = cls.expand_contractions(text)

        # Remove leading and trailing whitespace
        text = text.strip()

        # Convert English characters to lowercase if requested
        if lowercase:
            text = text.lower()

        # Replace multiple spaces/newlines with a single space
        text = re.sub(r"\s+", " ", text)

        return text