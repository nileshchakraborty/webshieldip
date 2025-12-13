import csv
from typing import Dict, List, Any

def load_anomaly_tables(filepath: str) -> List[Dict[str, Any]]:
    rules = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append({
                "feature": row['feature'],
                "min": float(row['bin_low_inclusive']),
                "max": float(row['bin_high_exclusive']),
                "score": float(row['anomaly_score'])
            })
    return rules

def get_anomaly_score(feature_name: str, value: float, rules: List[Dict[str, Any]]) -> float:
    for rule in rules:
        if rule['feature'] == feature_name:
            if rule['min'] <= value < rule['max']:
                return rule['score']
    return 0.0
