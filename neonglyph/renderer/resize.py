import cv2
import numpy as np

def calculate_dimensions(original_width: int, original_height: int, 
                         target_width: int = None, target_height: int = None, 
                         font_aspect_ratio: float = 0.55):
    """
    Calculates the new dimensions while preserving aspect ratio and compensating for terminal font.
    Most terminal fonts are roughly twice as tall as they are wide (approx 0.5 - 0.6 aspect ratio).
    """
    if target_width is None and target_height is None:
        target_width = 100 # Default width

    img_aspect_ratio = original_height / original_width
    
    if target_width:
        # Scale height based on width and font aspect ratio
        # height = width * image_aspect * font_aspect_ratio
        new_width = target_width
        new_height = int(new_width * img_aspect_ratio * font_aspect_ratio)
    else:
        # Scale width based on height
        new_height = target_height
        new_width = int(new_height / (img_aspect_ratio * font_aspect_ratio))
        
    return new_width, max(1, new_height)

def smart_resize(image: np.ndarray, target_width: int = None, target_height: int = None, font_aspect_ratio: float = 0.55) -> np.ndarray:
    """Resizes the image using high-quality interpolation."""
    h, w = image.shape[:2]
    new_w, new_h = calculate_dimensions(w, h, target_width, target_height, font_aspect_ratio)
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
