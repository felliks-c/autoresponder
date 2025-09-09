# app/nlp/pipeline.py
import spacy
from .intents import build_matcher, INTENT_TEMPLATES

class NLPPipeline:
    def __init__(self, model_name: str):
        self.nlp = spacy.load(model_name)
        self.matcher = build_matcher(self.nlp)

    def classify(self, text: str):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        if not matches:
            return "unknown", 0.0
        # простой приоритет: первый матч
        intent = self.nlp.vocab.strings[matches[0][0]]
        return intent, 0.9

    def respond(self, intent: str):
        return INTENT_TEMPLATES.get(intent, INTENT_TEMPLATES["unknown"])
