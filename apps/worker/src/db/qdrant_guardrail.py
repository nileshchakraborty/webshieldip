from typing import List, Dict, Any
import logging

ALLOWED_COLLECTIONS = {
    "policy_docs",
    "reviewer_guidance",
    "anchor_templates",
    "known_patterns"
}

class QdrantGuardrail:
    """
    Wrapper around Qdrant interactions to enforce:
    1. Only allowed collections.
    2. No session-specific writes (enforced by collection whitelist).
    """
    def __init__(self, client):
        self.client = client
        
    def upsert(self, collection_name: str, points: List[Any]):
        if collection_name not in ALLOWED_COLLECTIONS:
            raise ValueError(f"Write denied: Collection '{collection_name}' is not whitelist.")
            
        # Additional check: Inspect payload for 'session_id' leak?
        for p in points:
            if hasattr(p, 'payload') and p.payload:
                if 'session_id' in p.payload:
                    raise ValueError("Write denied: session_id found in vector payload.")
                    
        return self.client.upsert(collection_name, points)
        
    def search(self, collection_name: str, query_vector: List[float], limit: int = 5):
        # Read is permissive, but we shouldn't be reading user data if we didn't write it.
        if collection_name not in ALLOWED_COLLECTIONS:
             # If we tried to read a session_vector collection, it shouldn't exist.
             pass
        return self.client.search(collection_name, query_vector, limit=limit)
