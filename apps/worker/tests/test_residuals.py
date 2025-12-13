import unittest
from src.core.residuals import calculate_residual, get_residual_risk_score

class TestResiduals(unittest.TestCase):
    
    def test_calculation(self):
        # Medium exp = 90
        res = calculate_residual(30, "medium")
        self.assertEqual(res, -60) # 30 - 90
        
        res = calculate_residual(100, "medium")
        self.assertEqual(res, 10) # 100 - 90
        
    def test_risk_mapping(self):
        # Very fast
        score = get_residual_risk_score(-100)
        self.assertEqual(score, 0.9)
        
        # Normal
        score = get_residual_risk_score(10)
        self.assertEqual(score, 0.15)
        
        # Slow
        score = get_residual_risk_score(200)
        self.assertEqual(score, 0.20)

if __name__ == "__main__":
    unittest.main()
