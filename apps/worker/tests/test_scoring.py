import unittest
from src.core.scoring import calculate_risk_score, determine_band

class TestScoringRobustness(unittest.TestCase):
    
    def test_single_dimension_cap(self):
        # Even with 1.0 input, silence should be capped at 0.8
        dims = {"silence_s": 1.0}
        score = calculate_risk_score({}, dims)
        self.assertLessEqual(score, 0.8)
        self.assertNotEqual(determine_band(score), "enforce")
        
    def test_two_signal_rule_enforcement(self):
        # One high signal (0.9) -> Should be clamped below 0.85
        dims = {"silence_s": 0.9} 
        # Note: silence cap is 0.8, so let's use a non-capped pretend one or adjust cap via config
        config = {"dimension_caps": {"silence_s": 1.0, "other": 1.0}}
        
        score = calculate_risk_score({}, {"silence_s": 0.95}, config)
        self.assertLess(score, 0.85, "Should be clamped due to lack of 2 signals")
        
    def test_two_signal_rule_pass(self):
        # Two high signals -> Should pass through
        config = {"dimension_caps": {"dim1": 1.0, "dim2": 1.0}}
        dims = {"dim1": 0.9, "dim2": 0.7} # Both >= 0.6 (default threshold)
        
        score = calculate_risk_score({}, dims, config)
        # S = 1 - (0.1 * 0.3) = 1 - 0.03 = 0.97
        self.assertGreater(score, 0.85)
        
    def test_weak_residual(self):
        # Residual alone should be capped
        dims = {"residual": 0.9}
        score = calculate_risk_score({}, dims)
        # Cap is 0.5
        self.assertLessEqual(score, 0.5)
        
    def test_strong_residual_with_confirmation(self):
        # Residual + another signal -> allow high residual
        dims = {"residual": 0.9, "paste_burst_max": 0.7} 
        # paste cap is 0.7. paste=0.7 is >= 0.6 threshold.
        # So residual check: max_other=0.7 >= 0.6 -> True. 
        # Residual allowed 0.9. Paste allowed 0.7.
        # S = 1 - (0.1 * 0.3) = 0.97
        
        score = calculate_risk_score({}, dims)
        self.assertGreater(score, 0.9)

if __name__ == '__main__':
    unittest.main()
