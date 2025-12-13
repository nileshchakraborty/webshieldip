import requests
import time
import sys

API_URL = "http://localhost:3001/v1"

def test_e2e():
    print("Starting E2E Test (v2)...")
    
    # 1. Create Session
    session_id = f"test-{int(time.time())}"
    print(f"Creating session {session_id}")
    resp = requests.post(f"{API_URL}/sessions", json={
        "id": session_id,
        "deviceId": "test-device",
        "userId": "test-user",
        "assessmentId": "test-assessment"
    })
    
    if resp.status_code != 201:
        print(f"Failed to create session: {resp.text}")
        sys.exit(1)
        
    # 2. Send Event
    print("Sending events...")
    resp = requests.post(f"{API_URL}/sessions/{session_id}/events", json={
        "event_type": "question_shown",
        "ts_ms": int(time.time() * 1000),
        "payload": {"qid": "q1"}
    })
    
    if resp.status_code != 201:
        print(f"Failed to send event: {resp.text}")
        sys.exit(1)
        
    print("E2E Test Passed!")

if __name__ == "__main__":
    try:
        test_e2e()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
