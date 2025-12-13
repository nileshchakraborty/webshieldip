from typing import Dict

# Default expectations if config is missing
DEFAULT_EXPECTATIONS = {
    "easy": 45.0,
    "medium": 90.0,
    "hard": 160.0
}

def calculate_residual(completion_seconds: float, difficulty: str, config: Dict[str, float] = None) -> float:
    """
    Calculates the difficulty residual = observed_time - expected_time.
    
    Negative residual (completion < expected) -> Faster than expected (Risk increases if VERY fast).
    Positive residual (completion > expected) -> Slower than expected (Normal).
    """
    expectations = config if config else DEFAULT_EXPECTATIONS
    expected = expectations.get(difficulty.lower(), 90.0)
    
    return completion_seconds - expected

def get_residual_risk_score(residual: float) -> float:
    """
    Maps residual to a risk score (0-1).
    Heuristic:
    - Highly negative (<-90s) => 0.9 (Suspiciously fast)
    - Moderately negative (-45s) => 0.4
    - Normal/Positive => 0.1
    """
    if residual <= -90:
        return 0.9
    elif residual <= -45:
        return 0.7
    elif residual <= -15:
        return 0.4
    elif residual <= 15:
        return 0.15 # Normal variance
    else:
        return 0.2 # Slower is generally fine
