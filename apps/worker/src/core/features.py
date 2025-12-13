def extract_features(events):
    """
    Extracts features like silence_s, completion_s from a list of events.
    Input: List of event dicts
    Output: specialized feature dict
    """
    features = {
        "silence_s": 0.0,
        "completion_s": 0.0,
        "paste_burst_max": 0,
        "paste_chars_total": 0,
        "residual_s": 0.0
    }
    
    # Simple dummy logic for scaffolding
    start_time = None
    end_time = None
    
    for e in events:
        if e['type'] == 'question_shown':
            start_time = e['timestamp']
        if e['type'] == 'submit':
            end_time = e['timestamp']
            
    if start_time and end_time:
        features['completion_s'] = (end_time - start_time) / 1000.0
        
    return features
