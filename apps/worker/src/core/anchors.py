import time
from typing import Dict, List, Any, Optional

def should_trigger_anchor(session_events: List[Dict[str, Any]], 
                          existing_anchors: List[Dict[str, Any]],
                          config: Dict[str, Any],
                          current_risk_band: str) -> Optional[str]:
    """
    Determines if an anchor should be triggered based on policy bands and rate limits.
    Returns triggering reason string or None.
    
    Rules:
    1. Must be in 'anchors_required' band or higher (unless manual trigger).
    2. Spacing: At least N questions since last anchor.
    3. Cooldown: At least M seconds since last anchor.
    4. Max Count: Not exceeded session limit.
    """
    anchor_cfg = config.get("anchors", {})
    rate_limit = anchor_cfg.get("rate_limit", {})
    
    # 1. Band Check
    trigger_bands = ["anchors_required", "enforce"]
    if current_risk_band not in trigger_bands:
        return None
        
    # 2. Max Count Check
    max_count = rate_limit.get("max_count", {}).get("standard", 3)
    if len(existing_anchors) >= max_count:
        return None
        
    last_anchor_ts = 0
    last_anchor_idx = -1
    
    if existing_anchors:
        # Assuming existing_anchors are sorted or we find the max
        # and they have 'created_at' and 'question_index'
        # For this simplified model, we assume existing_anchors dicts have metadata
        sorted_anchors = sorted(existing_anchors, key=lambda x: x.get('created_at', 0))
        last = sorted_anchors[-1]
        last_anchor_ts = last.get('created_at', 0)
        last_anchor_idx = last.get('question_index', -1)

    # 3. Cooldown Check
    cooldown_sec = rate_limit.get("cooldown_seconds", 90)
    now_ms = time.time() * 1000 # Config is seconds, sys is ms usually? 
    # Let's standardize on standard Config inputs being raw numbers
    # If cooldown_seconds is 90, we need to compare vs (now - last)/1000
    
    if (time.time() - (last_anchor_ts / 1000.0)) < cooldown_sec:
        return None
        
    # 4. Spacing Check (Questions)
    # We need current question index. This function needs context of "where we are".
    # Assuming session_events is up to date, let's find current Q index.
    # This might require passing current_q_index explicitly.
    # For now, let's infer from the most recent 'question_shown' event
    
    # TODO: In real worker, current_q_index is passed. 
    # Let's add it to args in v2 if needed, or assume last event determines it.
    pass 
    
    return "risk_threshold"


def check_rate_limits(current_q_index: int,
                      current_ts_ms: int,
                      existing_anchors: List[Dict[str, Any]],
                      config: Dict[str, Any]) -> bool:
    """
    Helper to check strict rate limits.
    """
    anchor_cfg = config.get("anchors", {})
    rate_limit = anchor_cfg.get("rate_limit", {})
    
    # Max Count
    max_count = rate_limit.get("max_count", {}).get("standard", 3)
    if len(existing_anchors) >= max_count:
        return False

    if not existing_anchors:
        return True
        
    last = sorted(existing_anchors, key=lambda x: x.get('created_at', 0))[-1]
    
    # Cooldown
    cooldown_sec = rate_limit.get("cooldown_seconds", 90)
    if (current_ts_ms - last.get('created_at', 0)) / 1000.0 < cooldown_sec:
        return False
        
    # Spacing
    min_spacing = rate_limit.get("min_spacing_questions", 2)
    if (current_q_index - last.get('question_index', -1)) < min_spacing:
        return False
        
    return True

def evaluate_anchor_result(mcp_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hardened evaluation status.
    Uncertainty NEVER counts as failure.
    """
    passed = mcp_result.get("passed", False)
    uncertain = mcp_result.get("uncertain", False)
    
    if uncertain:
        # If uncertain, we consider it 'neutral' for enforcement, 
        # so effectively it didn't fail (but didn't pass either to lower risk).
        # Data model has passed=Boolean. 
        # API says: passed: True/False.
        # Logic: If uncertain, enforcement logic must treat it as NON-FAILURE.
        # We return explicit flags.
        return {"passed": False, "uncertain": True, "status": "uncertain"}
        
    return {
        "passed": passed, 
        "uncertain": False, 
        "status": "passed" if passed else "failed"
    }
