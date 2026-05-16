import cv2
import time
import sys
import msvcrt
import pickle
import os
from typing import Optional, List, Any, Dict
from .engine import ImageRenderer
from .utils import logger, console
from .themes import get_theme
from .morphing import PresetMorpher

class VideoRenderer:
    """
    Temporal renderer for video files and live streams.
    Features: HUD, Interactive Controls, Session Recording, and Preset Morphing.
    """
    
    def __init__(self, renderer: ImageRenderer):
        self.renderer = renderer

    def stream(self, 
               source: Any = 0, 
               width: int = 120, 
               mode: str = "grayscale",
               interactive: bool = False,
               fps: Optional[int] = None,
               record_path: Optional[str] = None,
               theme_name: str = "obsidian",
               morph: Optional[str] = None,
               morph_duration: float = 10.0,
               **render_kwargs):
        """
        Streams video from source with HUD and Live Morphing.
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            logger.error(f"Failed to open signal source: {source}")
            return

        params = {
            "mode": mode,
            "width": width,
            "gamma": render_kwargs.get("gamma", 1.0),
            "invert": render_kwargs.get("invert", False),
            "contrast": render_kwargs.get("contrast", False),
            "edge": render_kwargs.get("edge", False),
            "charset": render_kwargs.get("charset", "standard")
        }

        theme = get_theme(theme_name)
        recording = [] if record_path else None
        
        morpher = None
        if morph and ":" in morph:
            start_p, end_p = morph.split(":")
            morpher = PresetMorpher(start_p, end_p, morph_duration)

        import logging
        logging.getLogger("ascii_renderer").setLevel(logging.WARNING)

        target_delay = 1.0 / (fps if fps else 30)
        print("\033[2J\033[?25l", end="")
        
        try:
            while True:
                start_time = time.time()
                ret, frame = cap.read()
                if not ret:
                    break
                
                if source == 0:
                    frame = cv2.flip(frame, 1)
                
                # 1. Morphing Logic
                progress_pct = 0
                if morpher:
                    m_params, progress_pct = morpher.get_current_params()
                    params.update(m_params)
                    # For charset changes, we update the engine
                    self.renderer.charset = params.get("charset", "standard")

                # 2. Interactive Input
                if interactive and msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'q': params['gamma'] += 0.1
                    elif key == 'a': params['gamma'] = max(0.1, params['gamma'] - 0.1)
                    elif key == 'w': params['width'] += 5
                    elif key == 's': params['width'] = max(10, params['width'] - 5)
                    elif key == 'e': params['edge'] = not params['edge']
                    elif key == 'i': params['invert'] = not params['invert']
                    elif key == 'x': break

                # 3. Render Signal
                result = self.renderer.render_frame(
                    frame, 
                    width=params['width'], 
                    mode=params['mode'],
                    invert=params['invert'],
                    contrast=params["contrast"],
                    edge=params["edge"],
                    gamma=params["gamma"]
                )
                
                # 4. Construct HUD
                latency = (time.time() - start_time) * 1000
                fps_val = 1.0/max(0.001, time.time()-start_time)
                morph_info = f" | MORPH: {int(progress_pct*100)}%" if morpher else ""
                
                hud = [
                    f"╔══════════════════════════════════════════════════════════════╗",
                    f"║ NEONGLYPH PROJECTION | THEME: {theme_name.upper():<10} | FPS: {fps_val:.1f}{morph_info}  ║",
                    f"║ GAMMA: {params['gamma']:.1f} | WIDTH: {params['width']:<3} | EDGE: {'ON' if params['edge'] else 'OFF':<3} | LATENCY: {latency:.1f}ms ║",
                    f"╚══════════════════════════════════════════════════════════════╝"
                ]
                
                # 5. Raster Emission
                output_rows = result if isinstance(result, list) else result.plain.split("\n")
                full_frame = "\033[H"
                for line in hud: full_frame += line + "\n"
                full_frame += "\n".join(output_rows)
                
                if recording is not None: recording.append(full_frame)
                sys.stdout.write(full_frame)
                sys.stdout.flush()
                
                elapsed = time.time() - start_time
                if elapsed < target_delay: time.sleep(target_delay - elapsed)
                    
        except KeyboardInterrupt:
            pass
        finally:
            cap.release()
            print("\033[?25h")
            if recording and record_path:
                with open(record_path, 'wb') as f: pickle.dump(recording, f)
            print("\nStream Terminated.")
