import pytest
from app.core.tokenizer import (
    WordTokenizer,
    SentenceTokenizer
)


# ==========================================
# WordTokenizer Tests
# ==========================================

def test_english_word_tokenization():
    tokenizer = WordTokenizer()
    result = tokenizer.tokenize("I love Natural Language Processing!")
    assert result == ["I", "love", "Natural", "Language", "Processing", "!"]


def test_nepali_word_tokenization():
    tokenizer = WordTokenizer()
    result = tokenizer.tokenize("नेपाल राम्रो देश हो।")
    assert result == ["नेपाल", "राम्रो", "देश", "हो", "।"]


def test_english_contractions_and_hyphens():
    tokenizer = WordTokenizer()
    text = "Don't say it's user-friendly; we'll check it."
    result = tokenizer.tokenize(text)
    assert result == [
        "Don't", "say", "it's", "user", "-", "friendly",
        ";", "we'll", "check", "it", "."
    ]


def test_nepali_complex_conjuncts_and_modifiers():
    tokenizer = WordTokenizer()
    # Includes chandrabindu (ँ), anusvara (ं), halant/virama (्), ra-kars, and complex conjuncts
    text = "काठमाडौँमा धुलो, धुवाँ र अङ्ग्रेजी प्रविधि (AI) द्रुत गतिमा फैलियो।"
    result = tokenizer.tokenize(text)
    assert result == [
        "काठमाडौँमा", "धुलो", ",", "धुवाँ", "र", "अङ्ग्रेजी",
        "प्रविधि", "(", "AI", ")", "द्रुत", "गतिमा", "फैलियो", "।"
    ]


def test_nepali_devanagari_special_characters():
    tokenizer = WordTokenizer()
    # Visarga, Om, Rishi, rashtra, punarnirman
    text = "ॐ शान्ति! ऋषिले राष्ट्र पुनर्निर्माणको ज्ञान दिए।"
    result = tokenizer.tokenize(text)
    assert "ॐ" in result
    assert "ऋषिले" in result
    assert "राष्ट्र" in result
    assert "पुनर्निर्माणको" in result
    assert "ज्ञान" in result
    assert "!" in result
    assert "।" in result


def test_code_mixed_nepali_english_with_numbers():
    tokenizer = WordTokenizer()
    text = "२०८१ सालमा 5G र AI मोडल ९९.५% सफल भयो।"
    result = tokenizer.tokenize(text)
    assert "२०८१" in result
    assert "सालमा" in result
    assert "5G" in result
    assert "र" in result
    assert "AI" in result
    assert "मोडल" in result
    assert "९९" in result
    assert "%" in result
    assert "सफल" in result
    assert "भयो" in result


def test_word_tokenizer_type_error():
    tokenizer = WordTokenizer()
    with pytest.raises(TypeError, match="Input must be a string"):
        tokenizer.tokenize(None)

    with pytest.raises(TypeError, match="Input must be a string"):
        tokenizer.tokenize(12345)


# ==========================================
# SentenceTokenizer Tests
# ==========================================

def test_empty_sentence():
    tokenizer = SentenceTokenizer()
    assert tokenizer.tokenize("") == []
    assert tokenizer.tokenize("     ") == []


def test_sentence_tokenization_standard_english():
    tokenizer = SentenceTokenizer()
    result = tokenizer.tokenize("I love NLP. NLP is interesting! Are you ready?")
    assert result == [
        "I love NLP.",
        "NLP is interesting!",
        "Are you ready?"
    ]


def test_nepali_sentence_tokenization_with_dandas():
    tokenizer = SentenceTokenizer()
    # Tests single danda (।) and double danda (॥)
    text = "नेपाल एक सुन्दर देश हो। के तपाईं यहाँ आउनु भएको छ? अवश्य आउनुहोस्॥"
    sentences = tokenizer.tokenize(text)
    assert sentences == [
        "नेपाल एक सुन्दर देश हो।",
        "के तपाईं यहाँ आउनु भएको छ?",
        "अवश्य आउनुहोस्॥"
    ]


def test_sentence_tokenization_with_nepali_abbreviations():
    tokenizer = SentenceTokenizer()
    text = "डा. केसी र प्रा. शर्मा वि. सं. २०८१ मा भेटे। उनीहरूले छलफल गरे।"
    sentences = tokenizer.tokenize(text)
    assert len(sentences) == 2
    assert sentences[0] == "डा. केसी र प्रा. शर्मा वि. सं. २०८१ मा भेटे।"
    assert sentences[1] == "उनीहरूले छलफल गरे।"


def test_sentence_tokenization_with_english_titles_and_numbers():
    tokenizer = SentenceTokenizer()
    text = "Dr. Smith bought 3.14 liters of milk at 8.30 a.m. He then went home."
    sentences = tokenizer.tokenize(text)
    assert sentences == [
        "Dr. Smith bought 3.14 liters of milk at 8.30 a.m.",
        "He then went home."
    ]


def test_sentence_ending_within_quotations():
    tokenizer = SentenceTokenizer()
    text = "प्रधानमन्त्रीले भने, ‘यो राष्ट्रिय गौरवको आयोजना हो।’ त्यसपछि सबैले ताली बजाए।"
    sentences = tokenizer.tokenize(text)
    assert len(sentences) == 2
    assert sentences[0] == "प्रधानमन्त्रीले भने, ‘यो राष्ट्रिय गौरवको आयोजना हो।’"
    assert sentences[1] == "त्यसपछि सबैले ताली बजाए।"


def test_double_quotes_and_brackets_at_sentence_boundary():
    tokenizer = SentenceTokenizer()
    text = 'He shouted, "Stop right now!" (Everyone paused). Then silence prevailed.'
    sentences = tokenizer.tokenize(text)
    assert sentences == [
        'He shouted, "Stop right now!"',
        '(Everyone paused).',
        'Then silence prevailed.'
    ]


def test_multiple_consecutive_punctuation_marks():
    tokenizer = SentenceTokenizer()
    text = "साँच्चै हो??? मलाई थाहा छैन!! अर्को कुरा... पछि भनौंला।"
    sentences = tokenizer.tokenize(text)
    assert sentences == [
        "साँच्चै हो???",
        "मलाई थाहा छैन!!",
        "अर्को कुरा...",
        "पछि भनौंला।"
    ]


def test_multiline_sentences():
    tokenizer = SentenceTokenizer()
    text = """
    पहिलो हरफको वाक्य हो।
    दोस्रो हरफ यहाँ सुरू भयो!
    तेस्रो हरफ समाप्त भयो।
    """
    sentences = tokenizer.tokenize(text)
    assert sentences == [
        "पहिलो हरफको वाक्य हो।",
        "दोस्रो हरफ यहाँ सुरू भयो!",
        "तेस्रो हरफ समाप्त भयो।"
    ]


def test_sentence_without_ending_punctuation():
    tokenizer = SentenceTokenizer()
    text = "यसमा कुनै पूर्णविराम छैन"
    assert tokenizer.tokenize(text) == ["यसमा कुनै पूर्णविराम छैन"]


def test_sentence_tokenizer_custom_abbreviations():
    # Pass user-defined abbreviations
    tokenizer = SentenceTokenizer(custom_abbreviations=["का.म.पा.", "liab."])
    text = "का.म.पा. ले नयाँ नियम जारी गर्यो। यो राम्रो पहल हो।"
    sentences = tokenizer.tokenize(text)
    assert len(sentences) == 2
    assert sentences[0] == "का.म.पा. ले नयाँ नियम जारी गर्यो।"
    assert sentences[1] == "यो राम्रो पहल हो।"


def test_sentence_tokenizer_type_error():
    tokenizer = SentenceTokenizer()
    with pytest.raises(TypeError, match="Input must be a string"):
        tokenizer.tokenize(None)