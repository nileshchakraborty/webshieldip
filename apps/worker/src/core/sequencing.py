from typing import List, Dict, Any

def determine_sequencing(events: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Determines question indices deterministically based on 'first_shown_ts'.
    Returns: Dict[question_id, question_index]
    """
    # 1. Identify all questions and their first appearance
    q_start_times = {}
    
    for e in events:
        if e['event_type'] == 'question_shown':
            qid = e.get('question_id') or e['payload'].get('qid')
            ts = e['ts_ms']
            if qid:
                if qid not in q_start_times:
                    q_start_times[qid] = ts
                else:
                    q_start_times[qid] = min(q_start_times[qid], ts)
                    
    # 2. Sort by time, then ID
    sorted_qs = sorted(q_start_times.items(), key=lambda x: (x[1], x[0]))
    
    # 3. Assign index
    return {qid: idx for idx, (qid, _) in enumerate(sorted_qs)}
