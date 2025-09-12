from sentence_transformers import SentenceTransformer, util
import torch  # Для cosine similarity и GPU
from .intents import intent_datasets, default_responses
import json
import hashlib
from pathlib import Path

# Функция для создания хэша датасета (для проверки актуальности кэша)
def get_dataset_hash(dataset):
    dataset_str = json.dumps(dataset, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(dataset_str.encode('utf-8')).hexdigest()

# Функция для создания и кеширования эмбеддингов
def generate_embeddings(model_name='distiluse-base-multilingual-cased-v2', cache_file='embeddings.json'):
    # Загрузка модели
    model = SentenceTransformer(model_name)
    if torch.cuda.is_available():
        model = model.to('cuda')
        print("Используем GPU для вычислений эмбеддингов.")

    cache_path = Path(cache_file)
    # Проверяем, существует ли кэш и актуален ли он
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        # Проверяем хэши датасетов
        intent_hash = get_dataset_hash(intent_datasets)
        response_hash = get_dataset_hash(default_responses)
        if cache.get('intent_hash') == intent_hash and cache.get('response_hash') == response_hash:
            print("Загружаем эмбеддинги из кэша.")
            # Конвертируем списки в тензоры
            intent_embeddings = {intent: torch.tensor(data) for intent, data in cache['intent_embeddings'].items()}
            response_data = {
                intent: [(text, torch.tensor(emb)) for text, emb in data]
                for intent, data in cache['response_data'].items()
            }
            return intent_embeddings, response_data

    print("Кэш не найден или устарел. Вычисляем эмбеддинги.")
    # Прекомпьют эмбеддингов для вопросов (интентов)
    intent_embeddings = {}
    for intent, examples in intent_datasets.items():
        intent_embeddings[intent] = model.encode(examples, convert_to_tensor=True)

    # Прекомпьют эмбеддингов и текстов ответов
    response_data = {}
    for intent, responses in default_responses.items():
        embeddings = model.encode(responses, convert_to_tensor=True)
        response_data[intent] = list(zip(responses, embeddings))

    # Сохраняем в кэш
    cache = {
        'intent_hash': get_dataset_hash(intent_datasets),
        'response_hash': get_dataset_hash(default_responses),
        'intent_embeddings': {intent: emb.tolist() for intent, emb in intent_embeddings.items()},
        'response_data': {
            intent: [(text, emb.tolist()) for text, emb in data]
            for intent, data in response_data.items()
        }
    }
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False)
    print(f"Эмбеддинги сохранены в {cache_file}.")

    return intent_embeddings, response_data