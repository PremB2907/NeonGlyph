import numpy as np
import cv2
from typing import List
from .charset import get_braille_char

def map_pixels_to_ascii(image: np.ndarray, charset: str, invert: bool = False, gamma: float = 1.0) -> List[str]:
    """
    Vectorized mapping of pixels to ASCII using perceptual luminance and gamma correction.
    """
    if len(image.shape) == 3:
        # Perceptual luminance: 0.2126*R + 0.7152*G + 0.0722*B
        # OpenCV uses BGR
        weights = np.array([0.0722, 0.7152, 0.2126])
        image = np.dot(image[...,:3], weights)
    
    # Normalize to 0.0 - 1.0
    image = image.astype(float) / 255.0
    
    # Apply gamma correction
    if gamma != 1.0:
        image = np.power(image, gamma)
        
    if invert:
        image = 1.0 - image
        
    # Map back to charset indices
    num_chars = len(charset)
    indices = (image * (num_chars - 1)).astype(int)
    
    ascii_rows = []
    for row in indices:
        ascii_row = "".join([charset[idx] for idx in row])
        ascii_rows.append(ascii_row)
        
    return ascii_rows

def render_braille(image: np.ndarray, threshold: int = 127, invert: bool = False) -> List[str]:
    """
    Renders image using Braille characters.
    Maps 2x4 pixel blocks to a single Braille character.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    if invert:
        image = 255 - image
        
    # Binary thresholding
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    binary = (binary > 0).astype(int)
    
    h, w = binary.shape
    # Pad to multiples of 4 (height) and 2 (width)
    pad_h = (4 - (h % 4)) % 4
    pad_w = (2 - (w % 2)) % 2
    binary = np.pad(binary, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0)
    
    h, w = binary.shape
    rows = []
    for y in range(0, h, 4):
        row = ""
        for x in range(0, w, 2):
            block = binary[y:y+4, x:x+2]
            row += get_braille_char(block.tolist())
        rows.append(row)
    return rows

def apply_high_contrast(image: np.ndarray) -> np.ndarray:
    """Enhances image contrast using CLAHE."""
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(image)

def edge_detection(image: np.ndarray) -> np.ndarray:
    """Applies Canny edge detection."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    edges = cv2.Canny(gray, 100, 200)
    return edges
