from app.core.normalizer import TextNormalizer
from app.core.tokenizer import WordTokenizer
from app.languages.detector import LanguageDetector


class NLPPipeline:

    def __init__(self):

        self.normalizer = TextNormalizer()
        self.tokenizer = WordTokenizer()

    def process(self, text: str) -> dict:

        normalized = self.normalizer.normalize(text)

        tokens = self.tokenizer.tokenize(normalized)

        language = LanguageDetector.detect(normalized)

        return {
            "original_text": text,
            "normalized_text": normalized,
            "language": language,
            "tokens": tokens,
            "token_count": len(tokens)
        }