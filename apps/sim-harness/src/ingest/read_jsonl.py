import json
from typing import List, Dict, Any

def read_session_events(filepath: str) -> List[Dict[str, Any]]:
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    # Sort by timestamp to be safe
    events.sort(key=lambda x: x.get('ts_ms', 0))
    return events
