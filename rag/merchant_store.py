import json
from pathlib import Path

STORE_PATH = Path("data/merchant_memory.json")


def load_store() -> dict:
    if STORE_PATH.exists():
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))
    return {}


def save_store(store: dict):
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(store, indent=2))


def get_cached_category(merchant: str):
    store = load_store()
    return store.get(merchant.lower())


def cache_category(merchant: str, category: str):
    store = load_store()
    store[merchant.lower()] = category
    save_store(store)
