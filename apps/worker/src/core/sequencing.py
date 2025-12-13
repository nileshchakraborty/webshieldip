from typing import List, Dict, Any, Tuple

def normalize_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Dedupes and sorts events deterministically.
    """
    # 1. Deduplication (Idempotency Key = ID if present, else hash of content?)
    # Schema says 'id' is primary key, so we trust it unique.
    # However, if replay sends duplicates with SAME id, we assume they are identical.
    seen_ids = set()
    unique_events = []
    
    for e in events:
        eid = e.get('id')
        if eid and eid in seen_ids:
            continue
        if eid:
            seen_ids.add(eid)
        unique_events.append(e)
        
    # 2. Sort by ts_ms, then Event ID (lexical tie-break)
    # Ensure stable sort
    unique_events.sort(key=lambda x: (x.get('ts_ms', 0), x.get('id', '')))
    
    return unique_events

def determine_sequencing(events: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Determines question indices deterministically based on 'first_shown_ts'.
    Returns: Dict[question_id, question_index]
    """
    # 1. Identify all questions and their first appearance
    q_start_times = {}
    
    # Pre-requesite: Events should be roughly sorted, but we will find min ts anyway
    for e in events:
        if e['event_type'] == 'question_shown':
            qid = e.get('question_id') or (e.get('payload') or {}).get('question_id') or (e.get('payload') or {}).get('qid')
            ts = e.get('ts_ms', 0)
            if qid:
                if qid not in q_start_times:
                    q_start_times[qid] = ts
                else:
                    q_start_times[qid] = min(q_start_times[qid], ts)
                    
    # 2. Sort by time, then ID (Lexical Tie-Breaker for perfect determinism)
    sorted_qs = sorted(q_start_times.items(), key=lambda x: (x[1], x[0]))
    
    # 3. Assign index
    # 1-based index usually for readability? Or 0? Let's stick to 1-based for "Q1, Q2"
    return {qid: idx + 1 for idx, (qid, _) in enumerate(sorted_qs)}
