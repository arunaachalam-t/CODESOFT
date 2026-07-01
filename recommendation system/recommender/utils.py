import json
import math
from pathlib import Path


def load_json(filename: str) -> list | dict:
    path = Path(__file__).parent.parent / "data" / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    common_keys = set(vec_a) & set(vec_b)
    if not common_keys:
        return 0.0

    dot = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
