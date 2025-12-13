import unittest
from src.core.sequencing import normalize_events, determine_sequencing

class TestSequencing(unittest.TestCase):
    
    def test_deduplication(self):
        events = [
            {"id": "e1", "ts_ms": 100},
            {"id": "e1", "ts_ms": 100}, # Duplicate
            {"id": "e2", "ts_ms": 200}
        ]
        norm = normalize_events(events)
        self.assertEqual(len(norm), 2)
        self.assertEqual(norm[0]["id"], "e1")
        self.assertEqual(norm[1]["id"], "e2")
        
    def test_sorting(self):
        events = [
            {"id": "e3", "ts_ms": 300},
            {"id": "e1", "ts_ms": 100},
            {"id": "e2", "ts_ms": 200}
        ]
        norm = normalize_events(events)
        self.assertEqual([e["id"] for e in norm], ["e1", "e2", "e3"])
        
    def test_tie_breaking(self):
        # Same TS, use ID
        events = [
            {"id": "b", "ts_ms": 100},
            {"id": "a", "ts_ms": 100}
        ]
        norm = normalize_events(events)
        self.assertEqual(norm[0]["id"], "a")
        
    def test_question_indexing(self):
        events = [
            {"event_type": "question_shown", "ts_ms": 500, "payload": {"qid": "hard_q"}},
            {"event_type": "question_shown", "ts_ms": 100, "payload": {"qid": "easy_q"}},
            {"event_type": "other", "ts_ms": 50},
        ]
        
        # easy_q shown at 100. hard_q shown at 500.
        # Order: easy_q (1), hard_q (2)
        mapping = determine_sequencing(events)
        self.assertEqual(mapping["easy_q"], 1)
        self.assertEqual(mapping["hard_q"], 2)
        
    def test_question_indexing_tie_break(self):
        # Same TS
        events = [
            {"event_type": "question_shown", "ts_ms": 100, "payload": {"qid": "b"}},
            {"event_type": "question_shown", "ts_ms": 100, "payload": {"qid": "a"}},
        ]
        mapping = determine_sequencing(events)
        # a comes before b lexically
        self.assertEqual(mapping["a"], 1)
        self.assertEqual(mapping["b"], 2)

if __name__ == "__main__":
    unittest.main()
