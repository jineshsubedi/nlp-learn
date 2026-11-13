from app.core.pipeline import NLPPipeline

nlp = NLPPipeline()

text1 = "नेपालमा AI को बजार २०२६ मा NPR 10,000,000.001 सम्म पुग्न सक्छ!"
text2 = "I don’t really care about your problems"
text3 = "Maa I’m going to the market."
text4 = "He said, 'I can't go to the party because I'm grounded.'"
text5 = "What is the price of 1kg rice?"

result1 = nlp.process(text1)
result2 = nlp.process(text2)
result3 = nlp.process(text3)
result4 = nlp.process(text4)
result5 = nlp.process(text5)

print(result1)
print(result2)
print(result3)
print(result4)
print(result5)