import time
import os
import psycopg
import json
from db.postgres import get_connection
from core.features import extract_features
from core.sequencing import determine_sequencing
from llm.mcp import MCPClient
from llm.workflows import Workflows

def process_session(sess_id, conn):
    print(f"Processing session {sess_id}...")
    with conn.cursor() as cur:
        # 1. Fetch all events
        cur.execute("SELECT * FROM event_history WHERE session_id = %s ORDER BY ts_ms ASC", (sess_id,))
        rows = cur.fetchall()
        # Convert rows (tuples) to list of dicts for easier handling
        cols = [desc[0] for desc in cur.description]
        events = [dict(zip(cols, row)) for row in rows]
        
        if not events:
            return

        # 2. Sequencing
        q_indices = determine_sequencing(events)
        
        # 3. Per-Question Feature Extraction (Simplified loop)
        # Group by question
        events_by_q = {}
        for e in events:
            qid = e.get('question_id') or (e['payload'].get('qid') if e['payload'] else None)
            if qid:
                events_by_q.setdefault(qid, []).append(e)
                
        for qid, q_events in events_by_q.items():
            feats = extract_features(q_events) # utilizing existing extract_features
            idx = q_indices.get(qid, 0)
            
            # Upsert features
            cur.execute("""
                INSERT INTO question_features 
                (session_id, question_id, question_index, silence_s, completion_s, paste_burst_max, paste_chars_total)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id, question_id) DO UPDATE SET
                silence_s = EXCLUDED.silence_s,
                completion_s = EXCLUDED.completion_s
            """, (sess_id, qid, idx, feats['silence_s'], feats['completion_s'], feats['paste_burst_max'], feats['paste_chars_total']))

        conn.commit()
    print(f"Processed {sess_id}")

def main():
    print("Worker started (v2)...")
    mcp = MCPClient(get_connection())
    workflows = Workflows(mcp)
    
    # Polling loop (Simulated queue)
    while True:
        try:
            with get_connection() as conn:
                # Naive implementation: In real system, use NOTIFY/LISTEN or a jobs table
                # Here we just iterate 'active' sessions periodically
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM sessions WHERE status = 'active'")
                    sessions = cur.fetchall()
                    
                for (sess_id,) in sessions:
                    process_session(sess_id, conn)
                    
            time.sleep(5)
        except Exception as e:
            print(f"Worker Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
