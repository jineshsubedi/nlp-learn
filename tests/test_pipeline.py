import pytest
from app.core.entity import EntityRecognizer
from app.core.normalizer import TextNormalizer
from app.core.pipeline import NLPPipeline


# ---------------------------------------------------------
# Test Group 1: English Contractions Handling
# ---------------------------------------------------------
def test_english_contractions_expansion():
    normalizer = TextNormalizer()
    text = "I don't think Nepal's tech won't grow, they're ready and it's 2026."
    result = normalizer.normalize(text, expand_contractions=True)
    assert "do not" in result
    assert "will not" in result
    assert "they are" in result
    assert "it is" in result


def test_contractions_case_preservation():
    normalizer = TextNormalizer()
    text = "Don't worry, She'd love this NLP project."
    result = normalizer.expand_contractions(text)
    assert result.startswith("Do not")
    assert "She would" in result


# ---------------------------------------------------------
# Test Group 2: Nepali Unicode Normalization
# ---------------------------------------------------------
def test_nepali_unicode_normalization_danda_and_zwj():
    # Vertical pipe replaced by danda, and zero width space removed
    text = "हामी नेपाली हौँ | हामीलाई गर्व छ ।\u200b"
    result = TextNormalizer.normalize(text)
    assert "हामी नेपाली हौँ । हामीलाई गर्व छ ।" == result
    assert "\u200b" not in result


def test_nepali_unicode_nfd_to_nfc_with_modifiers():
    import unicodedata
    raw = "काठमाडौँ café"
    nfd = unicodedata.normalize("NFD", raw)
    assert not unicodedata.is_normalized("NFC", nfd)

    normalized = TextNormalizer.normalize(nfd)
    assert unicodedata.is_normalized("NFC", normalized)
    assert normalized == "काठमाडौँ café"


# ---------------------------------------------------------
# Test Group 3: Decimal Recognition
# ---------------------------------------------------------
def test_decimal_recognition_english_and_nepali():
    text = "The score was 3.1415 in English and ९९.५ in Devanagari."
    entities = EntityRecognizer.extract_decimals(text)
    values = [e["value"] for e in entities]
    assert 3.1415 in values
    assert 99.5 in values


def test_decimal_recognition_with_thousands_separators():
    text = "Total budget is 1,250.75 and १२,३४५.६० units."
    entities = EntityRecognizer.extract_decimals(text)
    values = [e["value"] for e in entities]
    assert 1250.75 in values
    assert 12345.6 in values


# ---------------------------------------------------------
# Test Group 4: Currency Recognition
# ---------------------------------------------------------
def test_currency_recognition_nepali_and_inr():
    text = "किताबको मूल्य रू. ५०० पर्छ, तर अनलाइनमा रू ५०.५० र ₹ 1,200 छ।"
    currencies = EntityRecognizer.extract_currencies(text)
    amounts = [c["amount"] for c in currencies]
    assert 500 in amounts
    assert 50.5 in amounts
    assert 1200 in amounts


def test_currency_recognition_international():
    text = "The software license is $49.99 or €120.00."
    currencies = EntityRecognizer.extract_currencies(text)
    assert len(currencies) == 2
    assert currencies[0]["symbol"] == "$"
    assert currencies[0]["amount"] == 49.99
    assert currencies[1]["symbol"] == "€"
    assert currencies[1]["amount"] == 120.00


# ---------------------------------------------------------
# Test Group 5: Complete NLP Pipeline
# ---------------------------------------------------------
def test_complete_nlp_pipeline_nepali():
    pipeline = NLPPipeline()
    text = "नेपालमा Artificial Intelligence को भविष्य राम्रो छ। यसले नयाँ अवसर ल्याउँछ।"
    result = pipeline.process(text)

    assert result["language"] == "ne"
    assert result["sentence_count"] == 2
    assert len(result["tokens"]) > 0
    assert "नेपालमा" in result["tokens"]
    assert "artificial" in result["tokens"]


def test_complete_nlp_pipeline_english_with_contractions_and_currencies():
    pipeline = NLPPipeline(clean_text=True, expand_contractions=True)
    text = "I don't think it's expensive at $150.75! Visit https://example.com for info."
    result = pipeline.process(text)

    assert result["language"] == "en"
    assert "do not" in result["normalized_text"]
    assert "it is" in result["normalized_text"]
    # URL removed by cleaner
    assert "https://example.com" not in result["normalized_text"]
    # Entity parsed
    assert len(result["entities"]["currencies"]) == 1
    assert result["entities"]["currencies"][0]["amount"] == 150.75


def test_complete_nlp_pipeline_mixed_language_code_mixing():
    pipeline = NLPPipeline()
    text = "नेपाल is beautiful"
    result = pipeline.process(text)
    assert result["language"] == "mixed"


def test_pipeline_type_error_on_invalid_input():
    pipeline = NLPPipeline()
    with pytest.raises(TypeError):
        pipeline.process(None)
