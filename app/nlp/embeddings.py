from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import torch
from .intents import intent_datasets, default_responses
import json
import hashlib
from pathlib import Path

CACHE_FILE = Path(__file__).parent / "embeddings.json"


def get_dataset_hash(dataset: dict) -> str:
    dataset_str = json.dumps(dataset, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(dataset_str.encode("utf-8")).hexdigest()


def generate_embeddings(
    model: SentenceTransformer | None = None,
    model_name: str = "distiluse-base-multilingual-cased-v2",
    device: str | None = None,
):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Try loading from cache first (no model needed for this)
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)

        intent_hash = get_dataset_hash(intent_datasets)
        response_hash = get_dataset_hash(default_responses)
        if (
            cache.get("intent_hash") == intent_hash
            and cache.get("response_hash") == response_hash
            and cache.get("model_name") == model_name
        ):
            intent_embeddings = {
                intent: torch.tensor(data).to(device)
                for intent, data in cache["intent_embeddings"].items()
            }
            response_data = {
                intent: [(text, torch.tensor(emb).to(device)) for text, emb in data]
                for intent, data in cache["response_data"].items()
            }
            return intent_embeddings, response_data

    # Cache miss — use provided model or create a new one
    if model is None:
        model = SentenceTransformer(model_name)
        if device == "cuda":
            model = model.to("cuda")

    intent_embeddings = {
        intent: model.encode(examples, convert_to_tensor=True)
        for intent, examples in intent_datasets.items()
    }

    response_data = {
        intent: list(zip(responses, model.encode(responses, convert_to_tensor=True)))
        for intent, responses in default_responses.items()
    }

    cache = {
        "model_name": model_name,
        "intent_hash": get_dataset_hash(intent_datasets),
        "response_hash": get_dataset_hash(default_responses),
        "intent_embeddings": {
            intent: emb.tolist() for intent, emb in intent_embeddings.items()
        },
        "response_data": {
            intent: [(text, emb.tolist()) for text, emb in data]
            for intent, data in response_data.items()
        },
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

    return intent_embeddings, response_data
