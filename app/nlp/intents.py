from spacy.matcher import PhraseMatcher

def build_matcher(nlp):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = {
        "greet": ["привет", "здравствуйте", "hello", "hi"],
        "bye": ["пока", "до свидания", "bye"],
        "weather": ["погода", "температура", "прогноз"],
        "about_company": ["о компании", "чем вы занимаетесь", "что вы делаете"],
    }
    for intent, phrases in patterns.items():
        matcher.add(intent, [nlp.make_doc(p) for p in phrases])
    return matcher

INTENT_TEMPLATES = {
  "greet": "Привет! Чем могу помочь?",
  "bye": "До связи! Хорошего дня.",
  "weather": "Мы пока не подключены к погодному API. Могу помочь с другим вопросом?",
  "about_company": "Мы разрабатываем ПО и помогаем автоматизировать процессы.",
  "unknown": "Я пока не понял запрос. Можете переформулировать?"
}
