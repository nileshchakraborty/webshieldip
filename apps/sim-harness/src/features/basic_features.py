from typing import List, Dict, Any

def extract_basic_features(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Group by question
    questions = {}
    for e in events:
        qid = e.get('question_id')
        if not qid: continue
        if qid not in questions:
            questions[qid] = []
        questions[qid].append(e)
        
    features_by_q = {}
    
    for qid, q_events in questions.items():
        # Find start and end
        q_shown = next((e for e in q_events if e['event_type'] == 'question_shown'), None)
        first_input = next((e for e in q_events if e['event_type'] == 'first_input'), None)
        submit = next((e for e in q_events if e['event_type'] == 'submit'), None)
        
        if not q_shown:
            continue
            
        start_ts = q_shown['ts_ms']
        input_ts = first_input['ts_ms'] if first_input else None
        submit_ts = submit['ts_ms'] if submit else (q_events[-1]['ts_ms'] if q_events else start_ts)
        
        # Calculate features
        silence_s = (input_ts - start_ts) / 1000.0 if input_ts else (submit_ts - start_ts) / 1000.0
        completion_s = (submit_ts - start_ts) / 1000.0
        
        # Paste calculation
        paste_events = [e for e in q_events if e['event_type'] == 'paste']
        paste_chars_total = sum(e['payload'].get('chars', 0) for e in paste_events)
        paste_burst_max = max([e['payload'].get('chars', 0) for e in paste_events]) if paste_events else 0
        
        # Backspace ratio (stub - assume 0 if no key events detail)
        # In real harness, we'd look at key aggregates.
        # For simulation, we might need 'payload.backspace_count'?
        # Let's assume input events have 'kind'='key' or 'paste'.
        # We'll rely on what's in the JSONL payload if available.
        backspace_ratio = 0.1 # Default 'normal' if unknown
        
        features_by_q[qid] = {
            "silence_s": silence_s,
            "completion_s": completion_s,
            "paste_chars_total": paste_chars_total,
            "paste_burst_max": paste_burst_max,
            "backspace_ratio": backspace_ratio,
            "difficulty": q_shown['payload'].get('difficulty', 'medium')
        }
        
    return features_by_q
