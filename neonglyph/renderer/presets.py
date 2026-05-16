from typing import Dict, Any

PRESETS: Dict[str, Dict[str, Any]] = {
    "noir": {
        "mode": "grayscale",
        "gamma": 1.4,
        "contrast": True,
        "charset": "extended",
        "effects": ["glow"]
    },
    "synthwave": {
        "mode": "color",
        "gamma": 1.1,
        "effects": ["glow", "scanlines"],
        "charset": "standard"
    },
    "crt": {
        "mode": "adaptive",
        "gamma": 1.2,
        "effects": ["scanlines", "glow", "decay"],
        "charset": "standard"
    },
    "matrix": {
        "mode": "matrix",
        "gamma": 1.0,
        "effects": ["noise", "decay"],
        "charset": "binary"
    },
    "ghost": {
        "mode": "braille",
        "gamma": 0.8,
        "effects": ["glow", "decay"],
        "invert": True
    },
    "cyberpunk": {
        "mode": "adaptive",
        "gamma": 1.3,
        "effects": ["glow", "scanlines", "noise"],
        "charset": "cyberpunk"
    }
}

def get_preset(name: str) -> Dict[str, Any]:
    return PRESETS.get(name.lower(), {})
