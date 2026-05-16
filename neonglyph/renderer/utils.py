import logging
import time
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

# Initialize Rich Console
console = Console()

def setup_logging(level=logging.INFO):
    """Sets up logging with Rich handler for beautiful terminal output."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    return logging.getLogger("ascii_renderer")

logger = setup_logging()

def get_output_path(input_path: str, suffix: str, output_dir: str = "outputs") -> Path:
    """Generates a unique output path based on input filename and suffix."""
    input_p = Path(input_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = int(time.time())
    return out_dir / f"{input_p.stem}_{timestamp}{suffix}"
