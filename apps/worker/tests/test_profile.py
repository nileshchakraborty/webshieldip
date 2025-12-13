import unittest
from src.core.profile import AccommodationProfile

class TestAccommodation(unittest.TestCase):
    
    def test_standard_profile(self):
        prof = AccommodationProfile("standard")
        scores = {"paste_frequency": 0.9, "typing_speed": 0.8}
        adj = prof.apply_dampeners(scores)
        self.assertEqual(adj, scores) # No change
        
    def test_screen_reader_profile(self):
        prof = AccommodationProfile("screen_reader")
        scores = {"paste_frequency": 0.9, "typing_speed": 0.8, "other": 0.5}
        adj = prof.apply_dampeners(scores)
        
        self.assertEqual(adj["paste_frequency"], 0.0) # Ignored
        self.assertEqual(adj["typing_speed"], 0.4)    # 0.8 * 0.5
        self.assertEqual(adj["other"], 0.5)           # Unaffected

if __name__ == "__main__":
    unittest.main()
