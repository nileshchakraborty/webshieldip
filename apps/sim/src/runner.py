import json
import time
import requests
import sys

API_URL = "http://localhost:3001/v1"

def run_simulation(file_path):
    print(f"Replaying session from {file_path}")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        # Create session
        session_id = f"sim-{int(time.time())}"
        requests.post(f"{API_URL}/sessions", json={
            "id": session_id,
            "deviceId": "sim-device",
            "userId": "sim-user",
            "assessmentId": "sim-assessment"
        })
        
        for line in lines:
            if not line.strip(): continue
            event = json.loads(line)
            
            # Ensure ts_ms exists
            if 'ts_ms' not in event:
                event['ts_ms'] = int(time.time() * 1000)
                
            # Send event
            resp = requests.post(f"{API_URL}/sessions/{session_id}/events", json=event)
            if resp.status_code != 201:
                print(f"Failed to send event: {resp.text}")
            
            # Simulate real-time delay?
            # time.sleep(0.01)
            
        print(f"Simulation completed for {session_id}")
        
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py <jsonl_file>")
    else:
        run_simulation(sys.argv[1])
