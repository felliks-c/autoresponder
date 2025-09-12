from sentence_transformers import SentenceTransformer, util
import torch  # Для cosine similarity и GPU
from .intents import default_responses
from .embeddings import intent_embeddings, response_embeddings
from .embeddings import generate_embeddings, intent_datasets, default_responses
from main import executor
import random
import asyncio
from concurrent.futures import ProcessPoolExecutor


# Шаг 1: Подготовка датасетов (маленькие наборы примеров для каждого интента)


# Шаг 2: Загрузка модели (многоязычная, поддерживает русский)
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Автоматическое использование GPU, если доступно
if torch.cuda.is_available():
    model = model.to('cuda')
    print("Используем GPU для вычислений.")


intent_embeddings, response_data = generate_embeddings()


# Функция для выбора ответа из интента
def select_response(intent, input_embedding):
    responses, embeddings = zip(*response_data[intent])
    embeddings = torch.stack(embeddings)
    similarities = util.cos_sim(input_embedding, embeddings)[0]
    max_sim = similarities.max().item()
    if len(set(similarities.tolist())) > 1 or max_sim > 0:
        best_index = similarities.argmax().item()
        return responses[best_index]
    else:
        return random.choice(responses)



# Функция классификации и выбора ответа
def classify_and_respond(user_input):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    
    max_sim_per_intent = {}
    avg_sim_per_intent = {}
    for intent, embeddings in intent_embeddings.items():
        similarities = util.cos_sim(input_embedding, embeddings)[0]
        max_sim_per_intent[intent] = similarities.max().item()
        avg_sim_per_intent[intent] = similarities.mean().item()
    
    candidates_max = {intent: max_sim for intent, max_sim in max_sim_per_intent.items() if max_sim > 0.7}
    if candidates_max:
        best_intent = max(candidates_max, key=candidates_max.get)
        response = select_response(best_intent, input_embedding)
        return best_intent, response
    
    candidates_avg = {intent: avg_sim for intent, avg_sim in avg_sim_per_intent.items() if avg_sim > 0.5}
    if candidates_avg:
        best_intent = max(candidates_avg, key=candidates_avg.get)
        response = select_response(best_intent, input_embedding)
        return best_intent, response
    
    best_intent = "непонятно"
    response = select_response(best_intent, input_embedding)
    return best_intent, response







# Примеры использования
# user_question = "Ты не знаешь о погоде?"
# intent, response = classify_and_respond(user_question)
# print(f"Классифицировано как: {intent}")
# print(f"Ответ: {response}\n")

# async def nlp_pipeline(user_input: str) -> str:
#     intent, response = classify_and_respond(user_input)
#     return response




async def nlp_pipeline_multi(user_input: str) -> str:
    # Запускаем синхронную функцию в пуле процессов
    # Это не блокирует event loop
    loop = asyncio.get_running_loop()
    intent, response = await loop.run_in_executor(
        executor,
        classify_and_respond,  # Функция, которую нужно запустить
        user_input                 # Аргументы для функции
    )
    return response