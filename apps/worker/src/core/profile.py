from typing import Dict, Any

class AccommodationProfile:
    def __init__(self, profile_name: str = "standard"):
        self.profile_name = profile_name
        self.dampeners = self._load_dampeners(profile_name)
    
    def _load_dampeners(self, profile: str) -> Dict[str, float]:
        """
        Loads risk dampening factors (0.0 - 1.0) for specific features.
        Risk = RawScore * Dampener
        """
        # In production this would come from a DB or secure config
        profiles = {
            "standard": {},
            "screen_reader": {
                "paste_frequency": 0.0, # Completely ignore paste (often used for inserting text chunks)
                "focus_switches": 0.2, # Heavily reduce risk from focus switching
                "typing_speed": 0.5    # Relax speed checks
            },
            "motor_impairment": {
                "typing_speed": 0.0,   # Ignore speed anomalies
                "backspace_ratio": 0.5 
            },
            "extended_time": {
                "time_to_completion": 0.5 # Relax duration checks
            }
        }
        return profiles.get(profile, {})

    def apply_dampeners(self, feature_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Adjusts raw feature scores based on the active accommodation profile.
        """
        adjusted = feature_scores.copy()
        for feature, score in adjusted.items():
            if feature in self.dampeners:
                dampener = self.dampeners[feature]
                adjusted[feature] = score * dampener
        return adjusted
