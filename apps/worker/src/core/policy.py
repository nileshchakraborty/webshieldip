from typing import Dict, Any, List, Optional

def check_completeness(evidence_bundle: Dict[str, Any]) -> bool:
    """
    Gates enforcement actions. Returns True if evidence is complete.
    
    Required Fields:
    - config_hash
    - scoring_version
    - created_at
    
    Content Requirements:
    - Must have 'features_snapshot'
    - Must have 'summary'
    """
    if not evidence_bundle:
        return False
        
    required_top_level = ["config_hash", "scoring_version", "created_at", "content"]
    for field in required_top_level:
        if field not in evidence_bundle or not evidence_bundle[field]:
            return False
            
    content = evidence_bundle.get("content", {})
    if not content:
        return False
        
    required_content = ["features_snapshot", "summary"]
    for field in required_content:
        if field not in content:
            return False
            
    # Deep check: Ensure model calls have IDs if present
    # (Assuming we pass model_calls list or it's embedded)
    # The spec says "model_call_ids recorded for any LLM-derived fields"
    # If we have anchors/entropy, we strictly need their Trace IDs.
    
    # Let's assume content includes 'anchors_snapshot' if anchors triggered
    anchors = content.get("anchors_snapshot", [])
    for anchor in anchors:
        if "model_call_id" not in anchor and "model_trace_id" not in anchor:
            # If it was an LLM anchor, it needs a trace.
            # If heuristics fallback, maybe not?
            # Hardening: Better safe. If it's an anchor event, we demand audit link.
            return False
            
    return True

def can_enforce(risk_band: str, evidence_bundle: Dict[str, Any]) -> bool:
    """
    Final gate.
    """
    if risk_band != "enforce":
        return True # Not enforcing, so strictness is lower? Or always strict?
        # "Policy must refuse to enforce if completeness check fails"
        # Implies strictly gating the transition to 'enforce' action.
        
    return check_completeness(evidence_bundle)
