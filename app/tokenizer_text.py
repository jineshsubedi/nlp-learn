from app.core.tokenizer import (
    WordTokenizer,
    SentenceTokenizer
)

text = "नेपाल राम्रो देश हो। I love Nepal!"
text2 = "जेन्सन हुआङ : एआईका बादशाहको निजी जीवनमा उठेका प्रश्न। हुआङको कठिन बाल्यकालदेखि एनभिडियाको सफलतासम्मको यात्रा असाधारण छ, तर चिनियाँ जासुस भनिएकी एलिस हुआङसँगको विवाहेतर सम्बन्धले उनको छविलाई धुमिल बनाएको छ।"
text3 = "डा. केसीले भने, ‘यो मेरो व्यक्तिगत लडाइँ मात्रै होइन, सम्पूर्ण मानव जातिको हो।’"

text4 = "I don't think Nepal's NLP industry is growing fast in 2026!"

word_tokenizer = WordTokenizer()
sentence_tokenizer = SentenceTokenizer()

print(word_tokenizer.tokenize(text))
print(sentence_tokenizer.tokenize(text))

print(word_tokenizer.tokenize(text2))
print(sentence_tokenizer.tokenize(text2))

print(word_tokenizer.tokenize(text3))
print(sentence_tokenizer.tokenize(text3))

print(word_tokenizer.tokenize(text4))
print(sentence_tokenizer.tokenize(text4))