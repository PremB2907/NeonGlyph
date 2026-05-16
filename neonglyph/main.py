import typer
import time
import json
import sys
from pathlib import Path
from typing import Optional, List
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.console import Console
from rich import print as rprint

from renderer.engine import ASCIIRenderer
from renderer.utils import setup_logging, get_output_path, console
from renderer.export import export_to_txt, export_to_html, export_to_png
from renderer.effects import (scanlines_effect, crt_glow_effect, vhs_noise_effect, 
                              phosphor_decay_effect, jitter_effect, tearing_effect, 
                              glitch_effect, projection_memory_effect)
from renderer.charset import calibrate_charset
from renderer.presets import get_preset
from renderer.video import VideoRenderer
from renderer.themes import get_theme

# Global Metadata
VERSION = "0.4.0"
TITLE = f"NEONGLYPH :: SIGNAL SYNTHESIS ENGINE v{VERSION}"

app = typer.Typer(help=TITLE, rich_markup_mode="rich", no_args_is_help=True)

def show_banner():
    banner = f"""
[bold cyan]
 ███╗   ██╗███████╗ ██████╗ ███╗   ██╗ ██████╗ ██╗     ██╗   ██╗██████╗ ██╗  ██╗
 ████╗  ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██║     ╚██╗ dress╝██╔══██╗██║  ██║
 ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║██║  ███╗██║      ╚████╔╝ ██████╔╝███████║
 ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║██║   ██║██║       ╚██╔╝  ██╔═══╝ ██╔══██║
 ██║ ╚████║███████╗╚██████╔╝██║ ╚████║╚██████╔╝███████╗   ██║   ██║     ██║  ██║
 ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝
[/bold cyan]
[bold white]{TITLE}[/bold white]
[italic dim]Interpretation over Reproduction. Signal atmospheres through glyph density.[/italic dim]
    """
    console.print(banner)

@app.command()
def synthesize(
    input_path: Optional[Path] = typer.Argument(None, help="Path to Signal Source (Image/Video)"),
    width: int = typer.Option(120, "--width", "-w", help="Projection Width"),
    height: Optional[int] = typer.Option(None, "--height", "-h", help="Projection Height"),
    mode: str = typer.Option("grayscale", "--mode", "-m", help="Synthesis Mode: grayscale, braille, color, matrix, adaptive"),
    preset: Optional[str] = typer.Option(None, "--preset", "-p", help="Neural Preset: noir, synthwave, crt, matrix, ghost, cyberpunk"),
    theme: str = typer.Option("obsidian", "--theme", "-t", help="Projection Theme: obsidian, amber, tokyo, matrix, ghost"),
    morph: Optional[str] = typer.Option(None, "--morph", help="Signal Morph (e.g., noir:cyberpunk)"),
    duration: float = typer.Option(10.0, "--duration", "-d", help="Morph Duration (seconds)"),
    charset: str = typer.Option("standard", "--charset", "-c", help="Glyph Set"),
    invert: bool = typer.Option(False, "--invert", "-i", help="Invert Signal"),
    contrast: bool = typer.Option(False, "--contrast", help="Enhance Contrast"),
    edge: bool = typer.Option(False, "--edge", help="Edge Detection Pass"),
    gamma: float = typer.Option(1.0, "--gamma", "-g", help="Gamma Correction"),
    effects: Optional[List[str]] = typer.Option(None, "--effect", "-f", help="Glyph Shaders: scanlines, glow, noise, decay, jitter, tearing, glitch"),
    calibrate: bool = typer.Option(False, "--calibrate", help="Calibrate Glyph Density"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Raster Emission: txt, html, png"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Emission Path"),
    webcam: bool = typer.Option(False, "--webcam", help="Live Neural Stream"),
    interactive: bool = typer.Option(False, "--interactive", help="Performance Mode"),
    record: Optional[str] = typer.Option(None, "--record", help="Record Session (.nglyph)"),
    play: Optional[str] = typer.Option(None, "--play", help="Playback Session (.nglyph)"),
    config: Optional[Path] = typer.Option(None, "--config", help="Neural Config (JSON)"),
):
    """Project a signal source into the terminal with cinematic adaptive shading."""
    show_banner()
    setup_logging()
    
    if play:
        video_engine = VideoRenderer(None)
        video_engine.play(play)
        return

    params = {
        "mode": mode, "charset": charset, "invert": invert, "contrast": contrast, 
        "edge": edge, "gamma": gamma, "theme": theme, "effects": effects or []
    }
    
    if preset:
        p_data = get_preset(preset)
        params.update(p_data)
    if config:
        with open(config, "r") as f:
            c_data = json.load(f)
            params.update(c_data)

    renderer = ASCIIRenderer(charset_name=params["charset"])
    if calibrate:
        rprint("[bold yellow]⚡ Calibrating Glyph Density...[/bold yellow]")
        renderer.engine.charset = calibrate_charset(renderer.engine.charset)
        
    for effect in params["effects"]:
        if effect == "scanlines": renderer.engine.add_effect(scanlines_effect)
        elif effect == "glow": renderer.engine.add_effect(crt_glow_effect)
        elif effect == "noise": renderer.engine.add_effect(vhs_noise_effect)
        elif effect == "decay": renderer.engine.add_effect(phosphor_decay_effect)
        elif effect == "jitter": renderer.engine.add_effect(jitter_effect)
        elif effect == "tearing": renderer.engine.add_effect(tearing_effect)
        elif effect == "glitch": renderer.engine.add_effect(glitch_effect)
        elif effect == "memory": renderer.engine.add_effect(projection_memory_effect)

    if webcam or interactive or morph or (input_path and input_path.suffix in ['.mp4', '.avi', '.mov']):
        video_engine = VideoRenderer(renderer.engine)
        source = 0 if (webcam or morph and input_path is None) else str(input_path)
        video_engine.stream(
            source=source, width=width, mode=params["mode"], interactive=interactive,
            record_path=record, theme_name=params["theme"], morph=morph, morph_duration=duration,
            invert=params["invert"], contrast=params["contrast"], edge=params["edge"], gamma=params["gamma"]
        )
        return

    if input_path is None:
        rprint("[bold red]Error:[/bold red] Signal source required.")
        raise typer.Exit(1)
        
    start_time = time.time()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task(description="Neural Signal Synthesis...", total=100)
        try:
            result = renderer.render(image_path=input_path, width=width, height=height, mode=params["mode"], invert=params["invert"], contrast=params["contrast"], edge=params["edge"], gamma=params["gamma"])
            progress.update(task, advance=80, description="Projecting Glyph Shaders...")
            theme_colors = get_theme(params["theme"])
            title = f"NeonGlyph :: {params['mode'].upper()}"
            if isinstance(result, list):
                console.print(Panel("\n".join(result), title=title, border_style=theme_colors["border"], padding=(1, 1)))
            else:
                console.print(Panel(result, title=title, border_style=theme_colors["border"], padding=(1, 1)))
            if export:
                progress.update(task, advance=10, description=f"Raster Emission...")
                suffix = f".{export}"
                out_path = output if output else get_output_path(input_path, suffix)
                rows = result if isinstance(result, list) else result.plain.split("\n")
                if export == "txt": export_to_txt(rows, out_path)
                elif export == "html": export_to_html(rows, out_path)
                elif export == "png": export_to_png(rows, out_path)
                rprint(f"[bold green]✓[/bold green] Signal emitted to [bold blue]{out_path}[/bold blue]")
            progress.update(task, advance=10, description="Synthesis Complete.")
        except Exception as e:
            rprint(f"[bold red]Neural Interruption:[/bold red] {e}")
            raise typer.Exit(code=1)

    duration_val = time.time() - start_time
    rprint(f"\n[bold cyan]Signal Metrics:[/bold cyan]")
    rprint(f" - Synthesis Pipeline: [yellow]{params['mode']}[/yellow] | Theme: [blue]{params['theme']}[/blue]")
    rprint(f" - Latency: [green]{duration_val:.3f}s[/green]")

if __name__ == "__main__":
    app()
