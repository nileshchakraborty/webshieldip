from typing import Dict, Any
import csv

def load_expectations(filepath: str) -> Dict[str, float]:
    expectations = {}
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expectations[row['difficulty']] = float(row['expected_seconds'])
    except FileNotFoundError:
        return {"easy": 45, "medium": 90, "hard": 160}
    return expectations

def compute_residual(completion_s: float, difficulty: str, expectations: Dict[str, float]) -> float:
    expected = expectations.get(difficulty, 90.0)
    return completion_s - expected
