import unittest
from src.core.policy import check_completeness, can_enforce

class TestPolicyGates(unittest.TestCase):
    
    def test_completeness_happy_path(self):
        bundle = {
            "config_hash": "abc",
            "scoring_version": "v1",
            "created_at": 12345,
            "content": {
                "features_snapshot": [{}],
                "summary": "Risk high",
                "anchors_snapshot": [{"id": "a1", "model_call_id": "trace_123"}]
            }
        }
        self.assertTrue(check_completeness(bundle))
        self.assertTrue(can_enforce("enforce", bundle))
        
    def test_missing_hash(self):
        bundle = {
            # missing config_hash
            "scoring_version": "v1",
            "created_at": 12345,
            "content": {"features_snapshot": [], "summary": "foo"}
        }
        self.assertFalse(check_completeness(bundle))
        self.assertFalse(can_enforce("enforce", bundle))
        
        # Valid if not enforcing? (Function returns True if band != enforce)
        self.assertTrue(can_enforce("observe", bundle))
        
    def test_missing_model_trace(self):
        bundle = {
            "config_hash": "abc",
            "scoring_version": "v1",
            "created_at": 12345,
            "content": {
                "features_snapshot": [],
                "summary": "foo",
                "anchors_snapshot": [{"id": "a1"}] # Missing trace
            }
        }
        self.assertFalse(check_completeness(bundle))

if __name__ == "__main__":
    unittest.main()
