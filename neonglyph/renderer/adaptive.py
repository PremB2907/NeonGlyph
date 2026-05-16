import cv2
import numpy as np
from typing import List, Union
from .grayscale import map_pixels_to_ascii, render_braille, edge_detection
from .charset import CharSet
from .resize import smart_resize

def adaptive_render(frame: np.ndarray, 
                    width: int = 120, 
                    charset: str = CharSet.STANDARD,
                    gamma: float = 1.0,
                    invert: bool = False) -> List[str]:
    """
    Cinematic Adaptive Rendering™:
    Combines edge-aware Braille rendering for details and density-aware ASCII for shadows.
    """
    # 1. Prepare dimensions for alignment
    # ASCII needs 1 pixel per character
    # Braille needs 2x4 pixels per character
    target_width = width
    
    # We use smart_resize to get the correct height based on font aspect ratio
    # For ASCII
    ascii_frame = smart_resize(frame, target_width=target_width)
    h, w = ascii_frame.shape[:2]
    
    # For Braille, we need 2x the width and 4x the height of the ASCII grid
    braille_frame = cv2.resize(frame, (w * 2, h * 4), interpolation=cv2.INTER_AREA)
    
    # 2. Generate layers
    # Edges should be detected on the Braille-scale frame for maximum detail
    edges = edge_detection(braille_frame)
    # Downsample edges to ASCII grid for masking
    edge_mask = cv2.resize(edges, (w, h), interpolation=cv2.INTER_AREA)
    _, edge_mask = cv2.threshold(edge_mask, 50, 255, cv2.THRESH_BINARY)
    
    # 3. Render base layers
    ascii_layer = map_pixels_to_ascii(ascii_frame, charset, invert=invert, gamma=gamma)
    braille_layer = render_braille(braille_frame, threshold=100, invert=invert)
    
    # 4. Intelligent Blending
    final_output = []
    for y in range(h):
        row = ""
        for x in range(w):
            if edge_mask[y, x] > 0:
                # Use Braille for edges
                row += braille_layer[y][x]
            else:
                # Use ASCII for smooth areas
                row += ascii_layer[y][x]
        final_output.append(row)
        
    return final_output
