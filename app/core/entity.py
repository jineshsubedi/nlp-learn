import re
from typing import TypedDict


class Entity(TypedDict):
    text: str
    kind: str
    value: float | str
    start: int
    end: int


class EntityRecognizer:
    """Extracts decimals, numbers (English & Devanagari), and currency amounts."""

    DEVANAGARI_DIGITS = {
        "०": "0", "१": "1", "२": "2", "३": "3", "४": "4",
        "५": "5", "६": "6", "७": "7", "८": "8", "९": "9",
    }

    # Matches Nepali/Indian/Western currencies and decimals
    # Examples:
    #   रू. ५००, रू ५०.५०, Rs. 1,000.50, $49.99, €12.50, ₹ 2,500
    CURRENCY_PATTERN = re.compile(
        r"(?P<symbol>Rs\.?|रू\.?|NPR|USD|EUR|GBP|INR|[$€£₹¥])\s*"
        r"(?P<amount>[\d०-९]+(?:[,][\d०-९]+)*(?:\.[\d०-९]+)?)",
        flags=re.IGNORECASE | re.UNICODE,
    )

    # Matches standalone decimal numbers (both Latin and Devanagari)
    # Examples: 3.1415, ०.७५, 1,234.56, १२,३४५.६७
    DECIMAL_PATTERN = re.compile(
        r"(?<![A-Za-z\u0900-\u097F$€£₹¥])(?P<num>[\d०-९]+(?:[,][\d०-९]+)*\.(?:[\d०-९]+)+)(?![A-Za-z\u0900-\u097F])",
        flags=re.UNICODE,
    )

    @classmethod
    def devanagari_to_ascii_digits(cls, text: str) -> str:
        """Converts Devanagari numerals (०-९) to ASCII digits (0-9)."""
        return "".join(cls.DEVANAGARI_DIGITS.get(ch, ch) for ch in text)

    @classmethod
    def parse_numeric_value(cls, text: str) -> float | int:
        """Cleans comma-formatted and Devanagari numbers into float or int."""
        clean = cls.devanagari_to_ascii_digits(text).replace(",", "").strip()
        return float(clean) if "." in clean else int(clean)

    @classmethod
    def extract_currencies(cls, text: str) -> list[dict]:
        """Extracts currency mentions with raw text, parsed amount, and currency unit."""
        currencies = []
        for match in cls.CURRENCY_PATTERN.finditer(text):
            raw_amount = match.group("amount")
            symbol = match.group("symbol")
            parsed_val = cls.parse_numeric_value(raw_amount)
            currencies.append({
                "text": match.group(0),
                "symbol": symbol,
                "amount": parsed_val,
                "start": match.start(),
                "end": match.end(),
            })
        return currencies

    @classmethod
    def extract_decimals(cls, text: str) -> list[dict]:
        """Extracts standalone decimal numbers."""
        decimals = []
        # Exclude regions already captured as currencies
        currency_spans = [
            (m.start(), m.end()) for m in cls.CURRENCY_PATTERN.finditer(text)
        ]

        for match in cls.DECIMAL_PATTERN.finditer(text):
            start, end = match.start(), match.end()
            # Skip if inside a currency match
            if any(c_start <= start and end <= c_end for c_start, c_end in currency_spans):
                continue

            raw_num = match.group("num")
            parsed_val = cls.parse_numeric_value(raw_num)
            decimals.append({
                "text": match.group(0),
                "value": parsed_val,
                "start": start,
                "end": end,
            })
        return decimals

    @classmethod
    def extract_all(cls, text: str) -> dict:
        """Extracts both currency and decimal entities from text."""
        return {
            "currencies": cls.extract_currencies(text),
            "decimals": cls.extract_decimals(text),
        }
