from app.core.cleaner import TextCleaner
from app.core.entity import EntityRecognizer
from app.core.normalizer import TextNormalizer
from app.core.tokenizer import SentenceTokenizer, WordTokenizer
from app.languages.detector import LanguageDetector


class NLPPipeline:
    """A complete bilingual (Nepali & English) NLP Pipeline."""

    def __init__(
        self,
        clean_text: bool = False,
        expand_contractions: bool = True,
        preserve_decimals: bool = False,
        preserve_currency: bool = False,
    ):
        self.clean_text = clean_text
        self.expand_contractions = expand_contractions
        self.preserve_decimals = preserve_decimals
        self.preserve_currency = preserve_currency

        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
        self.word_tokenizer = WordTokenizer()
        self.sentence_tokenizer = SentenceTokenizer()
        self.entity_recognizer = EntityRecognizer()

    def process(self, text: str) -> dict:
        """Runs the entire NLP pipeline on the given input text."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        # 1. Cleaning (optional: emails, URLs, excessive spaces)
        cleaned = self.cleaner.clean(text) if self.clean_text else text

        # 2. Extract entities before lowercasing to preserve exact currency symbols
        entities = self.entity_recognizer.extract_all(cleaned)

        # 3. Normalization (Unicode NFC, Nepali punctuation & ZWJ handling, contractions)
        normalized = self.normalizer.normalize(
            cleaned,
            expand_contractions=self.expand_contractions,
            lowercase=True,
        )

        # 4. Sentence Tokenization
        sentences = self.sentence_tokenizer.tokenize(cleaned)

        # 5. Word Tokenization
        tokens = self.word_tokenizer.tokenize(
            normalized,
            preserve_decimals=self.preserve_decimals,
            preserve_currency=self.preserve_currency,
        )

        # 6. Language Detection (Word-level ratio)
        language = LanguageDetector.detect(normalized)

        return {
            "original_text": text,
            "normalized_text": normalized,
            "language": language,
            "sentences": sentences,
            "sentence_count": len(sentences),
            "tokens": tokens,
            "token_count": len(tokens),
            "entities": entities,
        }