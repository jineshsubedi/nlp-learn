from app.core.pipeline import NLPPipeline

nlp = NLPPipeline()

result = nlp.process(
    "नेपालमा Artificial Intelligence को भविष्य राम्रो छ।"
)

print(result)