import numpy as np
from rich.text import Text
from rich.color import Color
from typing import List

def map_pixels_to_colored_ascii(image: np.ndarray, charset: str, invert: bool = False) -> Text:
    """
    Maps pixels to ASCII and applies original image colors using Rich Text.
    Assumes image is in BGR format (OpenCV default).
    """
    h, w, _ = image.shape
    
    # Convert to grayscale for character mapping
    import cv2
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if invert:
        gray = 255 - gray
        
    num_chars = len(charset)
    indices = (gray.astype(float) / 255.0 * (num_chars - 1)).astype(int)
    
    rich_text = Text()
    
    for y in range(h):
        for x in range(w):
            char = charset[indices[y, x]]
            b, g, r = image[y, x]
            # Rich uses RGB
            rich_text.append(char, style=f"rgb({r},{g},{b})")
        rich_text.append("\n")
        
    return rich_text

def matrix_effect(image: np.ndarray, charset: str = "01") -> Text:
    """Creates a Matrix-style green aesthetic."""
    h, w, _ = image.shape
    import cv2
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    num_chars = len(charset)
    indices = (gray.astype(float) / 255.0 * (num_chars - 1)).astype(int)
    
    rich_text = Text()
    for y in range(h):
        for x in range(w):
            char = charset[indices[y, x]]
            brightness = gray[y, x]
            # Green gradient based on brightness
            green_val = int(brightness)
            rich_text.append(char, style=f"rgb(0,{green_val},0)")
        rich_text.append("\n")
        
    return rich_text
