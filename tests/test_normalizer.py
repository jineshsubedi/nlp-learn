import pytest
import unicodedata
from app.core.normalizer import TextNormalizer


def test_english_normalization():
    text = "  HELLO    WORLD  "
    result = TextNormalizer.normalize(text)
    assert result == "hello world"


def test_nepali_normalization():
    text = "  नेपाल   राम्रो छ  "
    result = TextNormalizer.normalize(text)
    assert result == "नेपाल राम्रो छ"


def test_unicode_normalization_nfd_to_nfc():
    # Canonical decomposition (NFD) should be normalized to precomposed NFC
    nfd_text = unicodedata.normalize("NFD", "काठमाडौँमा café र résumé")
    # Verify input is indeed NFD and not NFC
    assert not unicodedata.is_normalized("NFC", nfd_text)

    result = TextNormalizer.normalize(nfd_text)

    # Must be valid NFC format
    assert unicodedata.is_normalized("NFC", result)
    assert result == "काठमाडौँमा café र résumé"


def test_mixed_whitespaces_and_newlines():
    text = "\t\n  HELLO \t\t  WORLD \n\r\n 2026 \t "
    result = TextNormalizer.normalize(text)
    assert result == "hello world 2026"


def test_code_mixed_nepali_english():
    text = "  NLP (प्राकृतिक भाषा प्रशोधन) : 100% ACCURATE!  "
    result = TextNormalizer.normalize(text)
    assert result == "nlp (प्राकृतिक भाषा प्रशोधन) : 100% accurate!"


def test_devanagari_conjuncts_and_chandrabindu():
    text = "  ॐ   शान्ति !   ऋषिले   पुनर्निर्माण   गरे ।  "
    result = TextNormalizer.normalize(text)
    assert result == "ॐ शान्ति ! ऋषिले पुनर्निर्माण गरे ।"


def test_empty_and_whitespace_only_strings():
    assert TextNormalizer.normalize("") == ""
    assert TextNormalizer.normalize("   ") == ""
    assert TextNormalizer.normalize("\t\n\r  \n") == ""


def test_already_normalized_string():
    text = "यो एक सामान्य वाक्य हो।"
    assert TextNormalizer.normalize(text) == text


def test_special_symbols_and_emojis():
    text = "   HELLO   🌍   WORLD!   🇳🇵   "
    result = TextNormalizer.normalize(text)
    assert result == "hello 🌍 world! 🇳🇵"


def test_type_error_on_invalid_input():
    with pytest.raises(TypeError, match="Input must be a string"):
        TextNormalizer.normalize(None)

    with pytest.raises(TypeError, match="Input must be a string"):
        TextNormalizer.normalize(12345)

    with pytest.raises(TypeError, match="Input must be a string"):
        TextNormalizer.normalize(["नेपाल"])