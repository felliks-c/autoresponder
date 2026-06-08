from sentence_transformers import SentenceTransformer, util
import torch
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .intents import default_responses
from .embeddings import generate_embeddings

MODEL_NAME = "distiluse-base-multilingual-cased-v2"

_device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"NLP: using {'GPU' if _device == 'cuda' else 'CPU'}")

# Load model once; reuse it for both cache generation and inference
model = SentenceTransformer(MODEL_NAME, device=_device)

# Generate or load embeddings from cache, passing model and device to avoid double-loading
intent_embeddings, response_data = generate_embeddings(model=model, model_name=MODEL_NAME, device=_device)

_executor = ThreadPoolExecutor(max_workers=4)

# Similarity thresholds for intent classification
_THRESHOLD_MAX = 0.62
_THRESHOLD_AVG = 0.45


def _select_response(intent: str, input_embedding) -> str:
    if intent == "непонятно":
        return random.choice(default_responses["непонятно"])

    pairs = response_data[intent]
    responses, embeddings = zip(*pairs)
    stacked = torch.stack(list(embeddings))
    similarities = util.cos_sim(input_embedding, stacked)[0]
    best_index = similarities.argmax().item()
    return responses[best_index]


def _classify_and_respond(user_input: str) -> tuple[str, str]:
    input_embedding = model.encode(user_input, convert_to_tensor=True)

    max_sims = {
        intent: util.cos_sim(input_embedding, embs)[0].max().item()
        for intent, embs in intent_embeddings.items()
    }
    avg_sims = {
        intent: util.cos_sim(input_embedding, embs)[0].mean().item()
        for intent, embs in intent_embeddings.items()
    }

    # Primary: intent with highest max similarity above threshold
    best_max_intent = max(max_sims, key=max_sims.get)
    if max_sims[best_max_intent] >= _THRESHOLD_MAX:
        return best_max_intent, _select_response(best_max_intent, input_embedding)

    # Fallback: intent with highest average similarity above threshold
    best_avg_intent = max(avg_sims, key=avg_sims.get)
    if avg_sims[best_avg_intent] >= _THRESHOLD_AVG:
        return best_avg_intent, _select_response(best_avg_intent, input_embedding)

    return "непонятно", _select_response("непонятно", input_embedding)


async def nlp_pipeline(user_input: str) -> tuple[str, str]:
    loop = asyncio.get_running_loop()
    intent, response = await loop.run_in_executor(_executor, _classify_and_respond, user_input)
    # returns (response, intent) to match existing callers
    return response, intent
