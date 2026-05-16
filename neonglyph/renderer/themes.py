from typing import Dict

THEMES: Dict[str, Dict[str, str]] = {
    "obsidian": {
        "border": "cyan",
        "title": "bold white",
        "hud_bg": "black",
        "accent": "cyan"
    },
    "amber": {
        "border": "orange3",
        "title": "bold orange3",
        "hud_bg": "black",
        "accent": "orange4"
    },
    "tokyo": {
        "border": "magenta",
        "title": "bold cyan",
        "hud_bg": "black",
        "accent": "deep_pink3"
    },
    "matrix": {
        "border": "green",
        "title": "bold green",
        "hud_bg": "black",
        "accent": "dark_green"
    },
    "ghost": {
        "border": "grey70",
        "title": "bold grey93",
        "hud_bg": "black",
        "accent": "grey30"
    }
}

def get_theme(name: str) -> Dict[str, str]:
    return THEMES.get(name.lower(), THEMES["obsidian"])
