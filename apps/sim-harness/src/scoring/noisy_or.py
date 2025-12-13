from typing import Dict

def compute_noisy_or(dimension_scores: Dict[str, float], weights: Dict[str, float]) -> float:
    # S_total = 1 - Prod(1 - w * S)
    prod = 1.0
    for dim, score in dimension_scores.items():
        w = weights.get(dim, 0.0)
        prod *= (1.0 - (w * score))
    return 1.0 - prod
