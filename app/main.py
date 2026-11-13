from app.core.normalizer import TextNormalizer
from app.core.cleaner import TextCleaner

text = """
    HELLO     WORLD!!!
    Visit https://example.com
    नेपाल राम्रो छ।
"""

normalized = TextNormalizer.normalize(text)
cleaned = TextCleaner.clean(normalized)

print(cleaned)