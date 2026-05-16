import time
from typing import Dict, Any, List
from .presets import get_preset

def interpolate_value(start: Any, end: Any, progress: float) -> Any:
    """Linearly interpolates between two values."""
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        return start + (end - start) * progress
    if isinstance(start, bool) and isinstance(end, bool):
        return start if progress < 0.5 else end
    # For lists (effects), we just switch at 0.5
    return start if progress < 0.5 else end

class PresetMorpher:
    """
    Interpolates between two neural presets over a specified duration.
    """
    def __init__(self, start_preset_name: str, end_preset_name: str, duration: float):
        self.start_params = get_preset(start_preset_name)
        self.end_params = get_preset(end_preset_name)
        self.duration = duration
        self.start_time = None
        
    def get_current_params(self) -> Dict[str, Any]:
        if self.start_time is None:
            self.start_time = time.time()
            
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        
        current_params = {}
        # Combine all keys from both presets
        all_keys = set(self.start_params.keys()).union(set(self.end_params.keys()))
        
        for key in all_keys:
            # Default values if key missing in one preset
            start_val = self.start_params.get(key, self.get_default_for_key(key))
            end_val = self.end_params.get(key, self.get_default_for_key(key))
            current_params[key] = interpolate_value(start_val, end_val, progress)
            
        return current_params, progress

    @staticmethod
    def get_default_for_key(key: str) -> Any:
        defaults = {
            "gamma": 1.0,
            "mode": "grayscale",
            "contrast": False,
            "invert": False,
            "charset": "standard",
            "effects": []
        }
        return defaults.get(key)
