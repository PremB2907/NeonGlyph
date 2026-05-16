import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Union, List, Any
from rich.text import Text
from abc import ABC, abstractmethod

from .resize import smart_resize
from .charset import CharSet
from .grayscale import map_pixels_to_ascii, apply_high_contrast, edge_detection, render_braille
from .color import map_pixels_to_colored_ascii, matrix_effect
from .adaptive import adaptive_render
from .effects import EffectPipeline, phosphor_decay_effect
from .utils import logger

class BaseRenderer(ABC):
    """Abstract base class for all renderers."""
    
    def __init__(self, charset_name: str = "standard"):
        self.charset = CharSet.get_charset(charset_name)
        self.pipeline = EffectPipeline()

    def add_effect(self, effect_func, **kwargs):
        self.pipeline.add(effect_func, **kwargs)

    @abstractmethod
    def render_frame(self, frame: np.ndarray, **kwargs) -> Any:
        pass

class ImageRenderer(BaseRenderer):
    """Renderer optimized for single images with adaptive support."""
    
    def render_frame(self, 
                    frame: np.ndarray, 
                    width: int = 120, 
                    height: Optional[int] = None,
                    mode: str = "grayscale",
                    invert: bool = False,
                    contrast: bool = False,
                    edge: bool = False,
                    gamma: float = 1.0) -> Union[List[str], Text]:
        
        # Pre-processing
        if contrast:
            frame = apply_high_contrast(frame)
        if edge:
            frame = edge_detection(frame)
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                
        # Apply shader pipeline
        frame = self.pipeline.apply(frame)
            
        # Resizing (different strategy for adaptive)
        if mode == "adaptive":
            # Adaptive uses its own internal layering logic but needs consistent width
            return adaptive_render(frame, width=width, charset=self.charset, gamma=gamma, invert=invert)
            
        res_width = width if mode != "braille" else width * 2
        frame = smart_resize(frame, target_width=res_width, target_height=height)
        
        # Rendering
        if mode == "grayscale":
            return map_pixels_to_ascii(frame, self.charset, invert=invert, gamma=gamma)
        elif mode == "braille":
            return render_braille(frame, invert=invert)
        elif mode == "color":
            return map_pixels_to_colored_ascii(frame, self.charset, invert=invert)
        elif mode == "matrix":
            return matrix_effect(frame)
        else:
            return map_pixels_to_ascii(frame, self.charset, invert=invert, gamma=gamma)

class ASCIIRenderer:
    """Orchestration class for NeonGlyph engine."""
    
    def __init__(self, charset_name: str = "standard"):
        self.engine = ImageRenderer(charset_name)
        
    def render(self, image_path: Union[str, Path], **kwargs) -> Any:
        logger.info(f"Loading image from {image_path}")
        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
        return self.engine.render_frame(image, **kwargs)

    def set_charset(self, charset_name: str):
        self.engine.charset = CharSet.get_charset(charset_name)
