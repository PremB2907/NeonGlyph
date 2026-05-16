import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def export_to_txt(ascii_rows: list, output_path: Path):
    """Exports ASCII art to a text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_rows))

def export_to_html(ascii_rows: list, output_path: Path, title: str = "ASCII Art", dark_mode: bool = True):
    """Exports ASCII art to an HTML file with CSS styling."""
    bg_color = "#000000" if dark_mode else "#ffffff"
    text_color = "#ffffff" if dark_mode else "#000000"
    
    ascii_joined = "\n".join(ascii_rows)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{
                background-color: {bg_color};
                color: {text_color};
                font-family: monospace;
                white-space: pre;
                line-height: 1;
                letter-spacing: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .ascii-art {{
                font-size: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="ascii-art">{ascii_joined}</div>
    </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def export_to_png(ascii_rows: list, output_path: Path, font_size: int = 15):
    """Renders ASCII art to a PNG image using PIL."""
    if not ascii_rows:
        return

    # Create a temporary image to calculate dimensions
    try:
        # Try to find a monospace font
        font = ImageFont.truetype("cour.ttf", font_size) # Courier New usually available on Windows
    except OSError:
        font = ImageFont.load_default()

    char_width, char_height = font.getbbox("A")[2:] # Rough estimate
    
    img_width = len(ascii_rows[0]) * (char_width + 1)
    img_height = len(ascii_rows) * (char_height + 1)
    
    img = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    y_offset = 0
    for row in ascii_rows:
        draw.text((0, y_offset), row, font=font, fill=(255, 255, 255))
        y_offset += char_height + 1
        
    img.save(output_path)
