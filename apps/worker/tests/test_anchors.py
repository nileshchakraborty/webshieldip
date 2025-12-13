import unittest
import time
from src.core.anchors import check_rate_limits, evaluate_anchor_result

class TestAnchorPolicy(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            "anchors": {
                "rate_limit": {
                    "min_spacing_questions": 2,
                    "cooldown_seconds": 90,
                    "max_count": {"standard": 3}
                }
            }
        }
        
    def test_rate_limit_cooldown(self):
        now = int(time.time() * 1000)
        recent_anchor = {"created_at": now - 30000} # 30s ago
        
        # Should fail cooldown (90s)
        allowed = check_rate_limits(10, now, [recent_anchor], self.config)
        self.assertFalse(allowed)
        
        old_anchor = {"created_at": now - 100000} # 100s ago
        allowed = check_rate_limits(10, now, [old_anchor], self.config)
        self.assertTrue(allowed)
        
    def test_rate_limit_spacing(self):
        now = int(time.time() * 1000)
        # Last anchor was at Q2. Current is Q3. Spacing is 1. Min is 2.
        anchor = {"created_at": now - 200000, "question_index": 2}
        
        allowed = check_rate_limits(3, now, [anchor], self.config)
        self.assertFalse(allowed)
        
        allowed = check_rate_limits(4, now, [anchor], self.config) # Spacing 2 -> Allowed?
        # Logic: (4 - 2) = 2. If min_spacing is 2, this typically means "wait 2 questions".
        # If Q2 had anchor, Q3 skip, Q4 allowed.
        self.assertTrue(allowed) # Wait, strictly: index diff >= min_spacing? 
        # (4-2)=2. >= 2. True.
        # Let's check my implementation logic: if (diff) < min_spacing. 
        # But wait, looking at my code: if (current - last) < min.
        # 2 < 2 is False. So it proceeds.
        # Wait, if min_spacing is 2.
        # Q2 -> Anchor. 
        # Q3 (diff 1). 1 < 2 -> Fail.
        # Q4 (diff 2). 2 < 2 -> False -> Pass.
        # So yes, Q4 allowed.
        # In this test I asserted False. I should fix expectation or code logic based on definition.
        # "no more than 1 anchor per 2 questions". Means: Anchor, Skip, Anchor is OK.
        # Anchor@Q2. Skip@Q3. Anchor@Q4. Gap is 1 question in between?
        # Typically "1 per 2" implies frequency. 50%.
        # Does "spacing 2" mean allow at Q2+2=Q4? Yes.
        # Let's correct test expectation to True.
        
    def test_max_count(self):
        now = int(time.time() * 1000)
        anchors = [{"created_at": 0}] * 3
        allowed = check_rate_limits(10, now, anchors, self.config)
        self.assertFalse(allowed)
        
    def test_uncertainty_is_not_failure(self):
        # Result from MCP
        mcp_res = {"passed": False, "uncertain": True}
        eval_res = evaluate_anchor_result(mcp_res)
        
        self.assertTrue(eval_res["uncertain"])
        self.assertEqual(eval_res["status"], "uncertain")
        # Ensure it didn't default to failed
        self.assertNotEqual(eval_res["status"], "failed")

if __name__ == "__main__":
    unittest.main()
