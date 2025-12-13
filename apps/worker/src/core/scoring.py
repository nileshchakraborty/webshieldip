from typing import Dict, List, Any

# Hardened Defaults
DIMENSION_CAPS = {
    "silence_s": 0.8,
    "completion_s": 0.9,
    "paste_burst_max": 0.7,
    "residual": 0.5  # Weak signal by default
}

TWO_SIGNAL_THRESHOLD = 0.6
POLICY_BANDS = [
    (0.0, "normal"),
    (0.3, "observe"),
    (0.5, "increase_sampling"),
    (0.7, "soft_clarification"),
    (0.85, "anchors_required"),
    (0.95, "enforce")
]

def calculate_risk_score(features: Dict[str, float], 
                         dimensions: Dict[str, float], 
                         config: Dict[str, Any] = None) -> float:
    """
    Calculates the aggregated risk score with hardening rules applied.
    
    Hardening Rules:
    1. Dimension Caps: No single dimension can exceed its cap.
    2. Weak Residual: Residual is capped low unless another signal matches.
    3. Two-Signal Rule: To exceed 0.85 (anchors_required), at least 2 dimensions 
       must be >= TWO_SIGNAL_THRESHOLD, OR a specific spike rule must trigger.
    """
    if config is None:
        config = {}
        
    caps = config.get("dimension_caps", DIMENSION_CAPS)
    
    # 1. Apply Caps
    capped_dims = {}
    for dim, score in dimensions.items():
        cap = caps.get(dim, 1.0)
        # Special case: Residual is weak usually
        if dim == "residual" and score > cap:
             # Check if any other dimension is high
            max_other = max([v for k,v in dimensions.items() if k != "residual"], default=0.0)
            if max_other < TWO_SIGNAL_THRESHOLD:
                capped_dims[dim] = min(score, cap)
            else:
                # If verified by another signal, allow full score (or higher cap)
                capped_dims[dim] = score
        else:
            capped_dims[dim] = min(score, cap)
            
    # 2. Aggregation (Noisy-OR)
    # S_total = 1 - product(1 - S_i)
    # We assume weights are already factorized into S_i or S_i are probabilities
    p_safe = 1.0
    for s in capped_dims.values():
        p_safe *= (1.0 - s)
    
    s_total = 1.0 - p_safe
    
    # 3. Two-Signal Rule
    # Count significant signals
    significant_signals = sum(1 for s in capped_dims.values() if s >= TWO_SIGNAL_THRESHOLD)
    
    # Check for specific "Spike" rule (e.g. huge paste burst) if configured
    is_spike = False # Implement if config requests
    
    if s_total >= 0.85:
        if significant_signals < 2 and not is_spike:
            # Clamp to below anchors_required if rule not met
            s_total = 0.84
            
    return round(s_total, 4)

def determine_band(score: float) -> str:
    for threshold, band in reversed(POLICY_BANDS):
        if score >= threshold:
            return band
    return "normal"
