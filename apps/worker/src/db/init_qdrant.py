import requests

QDRANT_URL = "http://vector-db:6333"

collections = [
    "policy_docs",
    "reviewer_guidance",
    "anchor_templates",
    "known_patterns"
]

def init_qdrant():
    for name in collections:
        try:
            resp = requests.put(f"{QDRANT_URL}/collections/{name}", json={
                "vectors": {
                    "size": 768, # assuming standard bert/embedding size, adjust as needed
                    "distance": "Cosine"
                }
            })
            print(f"Created collection {name}: {resp.status_code}")
        except Exception as e:
            print(f"Error creating {name}: {e}")

if __name__ == "__main__":
    init_qdrant()
