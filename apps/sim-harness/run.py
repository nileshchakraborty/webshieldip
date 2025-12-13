import argparse
import yaml
import os
import csv
from glob import glob
from src.ingest.read_jsonl import read_session_events
from src.features.basic_features import extract_basic_features
from src.features.difficulty_residual import load_expectations, compute_residual
from src.features.stubs import get_semantic_entropy_score, evaluate_anchor
from src.scoring.noisy_or import compute_noisy_or
from src.scoring.accumulate import accumulate_risk
from src.scoring.anomaly_map import load_anomaly_tables, get_anomaly_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--data', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
        
    decay = config['decay']
    weights = config['weights']
    thresholds = config['thresholds']
    
    # Load mappings
    expectations = load_expectations('apps/sim-harness/mappings/difficulty_expectations.csv')
    anomaly_rules = load_anomaly_tables('apps/sim-harness/mappings/anomaly_tables.csv')
    
    # Prepare output
    os.makedirs(args.out, exist_ok=True)
    out_csv = os.path.join(args.out, 'session_outcomes.csv')
    
    with open(out_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['session_id', 'final_risk', 'action', 'anchor_failures'])
        
        # Process datasets
        data_dirs = ['clean', 'assisted', 'partial_assist']
        for dtype in data_dirs:
            path = os.path.join(args.data, dtype, '*.jsonl')
            files = glob(path)
            
            for file in files:
                events = read_session_events(file)
                if not events: continue
                
                session_id = events[0]['session_id']
                basic_features = extract_basic_features(events)
                
                risk = 0.0
                anchor_failures = 0
                action = "observe"
                
                # Sort questions by start time to simulate stream
                sorted_qs = sorted(basic_features.keys(), 
                                 key=lambda q: [e['ts_ms'] for e in events if e.get('question_id')==q][0])
                
                for qid in sorted_qs:
                    feats = basic_features[qid]
                    
                    # 1. Feature -> Anomaly Score
                    silence_score = get_anomaly_score('silence_s', feats['silence_s'], anomaly_rules)
                    paste_score = get_anomaly_score('paste_burst_max', feats['paste_burst_max'], anomaly_rules)
                    
                    resid = compute_residual(feats['completion_s'], feats['difficulty'], expectations)
                    resid_score = get_anomaly_score('residual_s', resid, anomaly_rules)
                    
                    # Semantic (Stub)
                    # Need events for this question
                    q_events = [e for e in events if e.get('question_id') == qid]
                    semantic_score = get_semantic_entropy_score(q_events)
                    
                    # 2. Dimensions
                    # Mapping features to dimensions (simplified):
                    # Entropy = max(paste_score, semantic_score) ? Or avg?
                    # Let's say Input Entropy is predominantly paste & semantic.
                    # Temporal = silence_score ?
                    # Residual = resid_score
                    
                    dims = {
                        "entropy": max(paste_score, semantic_score),
                        "temporal": silence_score,
                        "residual": resid_score,
                        "semantic": semantic_score, # Duplicated? Weights handle it.
                        "focus": 0.0 # Stub
                    }
                    
                    # 3. Noisy OR
                    s_total = compute_noisy_or(dims, weights)
                    
                    # 4. Accumulate
                    risk = accumulate_risk(risk, s_total, decay)
                    
                    # 5. Policy Check
                    # Check for anchor
                    anchor_eval = evaluate_anchor(q_events)
                    if anchor_eval['triggered']:
                        if not anchor_eval['passed']:
                            anchor_failures += 1
                            
                    # Determine Action
                    if risk > thresholds['enforce'] and anchor_failures >= config['enforcement']['min_anchor_failures']:
                        action = "enforce"
                    elif risk > thresholds['anchors_required']:
                        action = "anchor_triggered" # Or soft_clarification
                        
                writer.writerow([session_id, f"{risk:.4f}", action, anchor_failures])
                print(f"Processed {session_id}: Risk={risk:.2f}, Action={action}")

if __name__ == "__main__":
    main()
