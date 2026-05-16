import cv2
import numpy as np

def scanlines_effect(frame: np.ndarray, intensity: float = 0.5) -> np.ndarray:
    """Adds horizontal scanlines to the frame."""
    h, w = frame.shape[:2]
    line_mask = np.ones((h, w), dtype=np.float32)
    line_mask[::2, :] = 1.0 - intensity
    
    if len(frame.shape) == 3:
        for i in range(3):
            frame[:,:,i] = (frame[:,:,i] * line_mask).astype(np.uint8)
    else:
        frame = (frame * line_mask).astype(np.uint8)
    return frame

def crt_glow_effect(frame: np.ndarray, radius: int = 15) -> np.ndarray:
    """Adds a soft bloom/glow effect similar to old CRT monitors."""
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    blur = cv2.GaussianBlur(frame, (0, 0), radius)
    glow = cv2.addWeighted(frame, 1.0, blur, 0.5, 0)
    return glow

def vhs_noise_effect(frame: np.ndarray, noise_level: float = 0.1) -> np.ndarray:
    """Adds random grain/noise to the frame."""
    noise = np.random.randint(0, int(255 * noise_level), frame.shape, dtype='uint8')
    return cv2.add(frame, noise)

def jitter_effect(frame: np.ndarray, intensity: int = 2) -> np.ndarray:
    """Simulates signal instability by randomly shifting frame rows."""
    h, w = frame.shape[:2]
    new_frame = frame.copy()
    for i in range(h):
        if np.random.random() < 0.1: # 10% chance per row
            shift = np.random.randint(-intensity, intensity + 1)
            new_frame[i] = np.roll(frame[i], shift, axis=0)
    return new_frame

def tearing_effect(frame: np.ndarray, probability: float = 0.05) -> np.ndarray:
    """Simulates frame tearing / raster collapse."""
    if np.random.random() > probability:
        return frame
    h, w = frame.shape[:2]
    tear_point = np.random.randint(0, h)
    new_frame = frame.copy()
    shift = np.random.randint(5, 15)
    new_frame[tear_point:] = np.roll(frame[tear_point:], shift, axis=1)
    return new_frame

def glitch_effect(frame: np.ndarray, intensity: float = 0.05) -> np.ndarray:
    """Injects digital artifacts and color channel shifts."""
    if np.random.random() > intensity:
        return frame
    
    # Random channel swap
    if len(frame.shape) == 3:
        channels = [0, 1, 2]
        np.random.shuffle(channels)
        frame = frame[:, :, channels]
    return frame

def phosphor_decay_effect(current_frame: np.ndarray, previous_frame: np.ndarray, decay_rate: float = 0.6) -> np.ndarray:
    """Simulates CRT phosphor persistence by blending current and previous frames."""
    if previous_frame is None:
        return current_frame
    return cv2.addWeighted(current_frame, 1.0 - decay_rate, previous_frame, decay_rate, 0)

def projection_memory_effect(current_frame: np.ndarray, memory_buffer: np.ndarray, persistence: float = 0.05) -> np.ndarray:
    """
    Simulates 'Emotional Residue' where previous projection states leave 
    subtle, long-term textual ghosts on the terminal landscape.
    """
    if memory_buffer is None:
        return current_frame, current_frame.copy()
    
    # Update memory buffer with a tiny fraction of the current frame
    memory_buffer = cv2.addWeighted(memory_buffer, 0.98, current_frame, 0.02, 0)
    
    # Blend the memory buffer into the current frame
    output = cv2.addWeighted(current_frame, 1.0 - persistence, memory_buffer, persistence, 0)
    
    return output, memory_buffer

class EffectPipeline:
    """Helper to chain effects together with temporal state awareness."""
    def __init__(self):
        self.effects = []
        self.prev_frame = None
        self.memory_buffer = None

    def add(self, effect_func, **kwargs):
        self.effects.append((effect_func, kwargs))

    def apply(self, frame: np.ndarray) -> np.ndarray:
        for effect_func, kwargs in self.effects:
            if effect_func.__name__ == 'phosphor_decay_effect':
                frame = effect_func(frame, self.prev_frame, **kwargs)
            elif effect_func.__name__ == 'projection_memory_effect':
                frame, self.memory_buffer = effect_func(frame, self.memory_buffer, **kwargs)
            else:
                frame = effect_func(frame, **kwargs)
        
        self.prev_frame = frame.copy()
        return frame
