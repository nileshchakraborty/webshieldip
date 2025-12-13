def accumulate_risk(prev_risk: float, current_signal: float, decay: float) -> float:
    # R_t = min(1, decay * R_t-1 + S_total)
    return min(1.0, (decay * prev_risk) + current_signal)
