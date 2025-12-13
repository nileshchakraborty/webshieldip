import unittest
from unittest.mock import MagicMock
from src.db.qdrant_guardrail import QdrantGuardrail

class TestStoreGuardrails(unittest.TestCase):
    
    def setUp(self):
        self.mock_client = MagicMock()
        self.guard = QdrantGuardrail(self.mock_client)
        
    def test_allowed_write(self):
        self.guard.upsert("policy_docs", [])
        self.mock_client.upsert.assert_called()
        
    def test_forbidden_collection_write(self):
        with self.assertRaises(ValueError) as cm:
            self.guard.upsert("user_sessions", [])
        self.assertIn("not whitelist", str(cm.exception))
        
    def test_session_id_leak_prevention(self):
        # Emulate a point object
        class Point:
            def __init__(self, payload):
                self.payload = payload
                
        p = Point({"session_id": "123", "text": "sensitive"})
        
        with self.assertRaises(ValueError) as cm:
            self.guard.upsert("policy_docs", [p])
        self.assertIn("session_id found", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
