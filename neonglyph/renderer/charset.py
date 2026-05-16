import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Optional

class CharSet:
    """Character sets for different rendering styles."""
    
    STANDARD = "@%#*+=-:. "
    EXTENDED = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    BLOCK = "█▓▒░ "
    MINIMAL = "#+- "
    BINARY = "01 "
    CYBERPUNK = "日片月火水木金土"
    
    @staticmethod
    def get_charset(name: str) -> str:
        charsets = {
            "standard": CharSet.STANDARD,
            "extended": CharSet.EXTENDED,
            "block": CharSet.BLOCK,
            "minimal": CharSet.MINIMAL,
            "binary": CharSet.BINARY,
            "cyberpunk": CharSet.CYBERPUNK
        }
        return charsets.get(name.lower(), CharSet.STANDARD)

def get_braille_char(binary_block: List[List[int]]) -> str:
    """Converts a 2x4 binary block into a Braille unicode character."""
    dots = [
        binary_block[0][0], binary_block[1][0], binary_block[2][0],
        binary_block[0][1], binary_block[1][1], binary_block[2][1],
        binary_block[3][0], binary_block[3][1]
    ]
    res = 0
    for i, dot in enumerate(dots):
        if dot:
            res += (1 << i)
    return chr(0x2800 + res)

def calibrate_charset(charset: str, font_path: Optional[str] = None, font_size: int = 20) -> str:
    """
    Measures actual pixel density of characters and sorts them from darkest to lightest.
    """
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Fallback to Courier New if on Windows
            font = ImageFont.truetype("cour.ttf", font_size)
    except:
        font = ImageFont.load_default()

    densities = []
    for char in charset:
        # Create a small image for each char
        img = Image.new('L', (font_size, font_size * 2), color=255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), char, font=font, fill=0)
        
        # Calculate density (ratio of black pixels)
        arr = np.array(img)
        density = np.sum(arr == 0) / arr.size
        densities.append((char, density))
    
    # Sort by density (descending: darkest first)
    sorted_chars = sorted(densities, key=lambda x: x[1], reverse=True)
    return "".join([c[0] for c in sorted_chars])
