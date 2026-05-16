# 🌌 NeonGlyph – Signal Synthesis & Terminal Projection Engine

> "The terminal is not a console. It's a phosphor‑lit landscape."

**NeonGlyph** is a *terminal‑native visual synthesizer* that turns images, video, or live webcam streams into cinematic glyph landscapes. It treats the terminal as a **dreaming phosphor organism** – a medium that **interprets**, **distorts**, **remembers**, and **evolves**.

---

## 📖 Table of Contents
1. [Philosophy & Principles](#philosophy--principles)  
2. [Features at a Glance](#features-at-a-glance)  
3. [Installation](#installation)  
4. [Quick‑Start Usage](#quick‑start-usage)  
5. [Advanced Commands](#advanced-commands)  
6. [Projection Packs (Ecosystems)](#projection-packs-ecosystems)  
7. [Technical Architecture](#technical-architecture)  
8. [Contribution Guide](#contribution-guide)  
9. [License](#license)  
10. [Acknowledgements](#acknowledgements)

---

## 🌠 Philosophy & Principles
| Principle | Manifestation |
|-----------|---------------|
| **Interpretation over Reproduction** | Adaptive rendering that favours atmospheric shading over pixel‑perfect fidelity. |
| **Instability as Aesthetic** | Jitter, tearing, glitch, and signal fatigue become visual vocabularies. |
| **Memory & Residue** | **Projection Memory™** creates lingering glyph ghosts, turning the terminal into a *temporal canvas*. |
| **Atmospheric Identity** | Themes and Packs give each run a distinct cinematic personality. |
| **Temporal Emotion** | Morphing interpolates between moods, enabling narrative arcs. |
| **Phosphor Aesthetics** | Scanlines, bloom, decay – all inspired by CRT displays and analog film. |
| **Machine Presence** | HUD & instrumentation expose the engine’s inner state, making the terminal a *performer*. |

> **NeonGlyph is not just a renderer.** It is a *medium‑first* creative tool that invites you to compose, not just convert.

---

## ⚡ Features at a Glance
- **Cinematic Adaptive Rendering™** – layered Braille‑detail + ASCII‑density shading. 
- **Signal Morphing** – real‑time interpolation between visual presets (`--morph noir:cyberpunk`).
- **Projection Memory™** – long‑term emotional residue; past frames leave subtle glyph ghosts.
- **Signal Corruption Shaders** – `jitter`, `tearing`, `glitch`, `decay`, `memory`.
- **Live Neural Streaming** – webcam or video file streaming with a low‑latency HUD.
- **ANSI Session Recording** – `.nglyph` binary format for deterministic playback.
- **Projection Packs** – curated ecosystems (`Neo‑Tokyo`, `Archive‑79`, `Spectral`, `Collapse`).
- **Rich CLI** – Typer‑based command with auto‑completion, theming, and interactive performance mode.
- **Export Options** – `.txt`, `.html`, `.png` for offline use.
- **Extensible Effect Pipeline** – plug‑in new shaders with a single function.

---

## 📦 Installation
```bash
# Clone the repo (already done) and cd into the project root
git clone https://github.com/PremB2907/NeonGlyph.git
cd NeonGlyph

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r neonglyph/requirements.txt
```
> **Python 3.11+** is required.

---

## 🚀 Quick‑Start Usage
```bash
# Basic image synthesis with a theme
python neonglyph/main.py \
    neonglyph/assets/sample_images/sample_portrait.jpg \
    --theme amber --width 80

# Live webcam with interactive controls
python neonglyph/main.py --webcam --interactive --preset cyberpunk --theme tokyo

# Morph from noir to cyberpunk over 12 seconds while preserving memory
python neonglyph/main.py \
    neonglyph/assets/sample_images/sample_portrait.jpg \
    --morph noir:cyberpunk --duration 12 --effect memory
```
All commands show a HUD with FPS, latency, current theme, and morph progress.

---

## 🛠️ Advanced Commands
| Flag | Description |
|------|-------------|
| `--preset <name>` | Load a preset from `neonglyph/renderer/presets.py`. |
| `--theme <name>` | Choose a visual identity (`obsidian`, `amber`, `tokyo`, `matrix`, `ghost`). |
| `--effect <shader>` | Add a shader (`scanlines`, `glow`, `noise`, `decay`, `jitter`, `tearing`, `glitch`, `memory`). |
| `--morph <a:b>` | Interpolate between two presets (`a` → `b`). |
| `--duration <seconds>` | Length of the morph transition. |
| `--record <file.nglyph>` | Record the session to a native `.nglyph` file. |
| `--play <file.nglyph>` | Playback a recorded session. |
| `--fatigue` | Enable Signal Fatigue™ – gradual intensification of decay, jitter, and memory over time. |
| `--recursive --depth <n>` | Render NeonGlyph inside itself for *n* recursion levels (experimental). |
| `--pack <name>` | Load a Projection Pack JSON from `packs/`. |

---

## 📚 Projection Packs (Ecosystems)
Projection Packs are **curated collections** of presets, themes, effect weightings, and optional fatigue curves. They let you select a *mood* rather than a stack of individual flags.

### Example Packs (included in `packs/`)
| Pack | Presets | Theme | Vibe |
|------|---------|-------|------|
| **Neo‑Tokyo** | `cyberpunk`, `synthwave` | `tokyo` | Neon‑rain, high‑frequency glitch. |
| **Archive‑79** | `crt`, `matrix` | `amber` | Analog phosphor burn‑in, green entropy. |
| **Spectral** | `ghost`, `noir` | `ghost` | Pale, haunting grayscale, long‑term memory ghosting. |
| **Collapse** | `matrix` + `glitch` | `matrix` | Unstable, tearing, rapid fatigue. |

To use a pack:
```bash
python neonglyph/main.py input.jpg --pack neo_tokyo --width 100
```
You can add your own packs by dropping a JSON file into `packs/`:
```json
{
  "preset": "cyberpunk",
  "theme": "tokyo",
  "effects": ["glitch", "memory"],
  "fatigue": true,
  "fatigue_curve": {"decay": 0.02, "jitter": 0.01}
}
```

---

## 🏛️ Technical Architecture
````mermaid
flowchart TD
    A[Signal Ingestion] --> B[Perceptual Synthesis]
    B --> C[Adaptive Layering]
    C --> D[Glyph Shading]
    D --> E[Signal Corruption]
    E --> F[Temporal Persistence]
    F --> G[Neural Morphing]
    G --> H[Projection Memory™]
    H --> I[Projection Emission]
````
- **Engine** – `renderer/engine.py` handles core image conversion and adaptive blending.
- **Effects** – Stateless shaders (scanlines, glow) and stateful ones (decay, memory) live in `renderer/effects.py`.
- **Morphing** – `renderer/morphing.py` interpolates preset dictionaries over time.
- **Video** – `renderer/video.py` provides live streaming, HUD, and interactive controls.
- **Themes & Packs** – `renderer/themes.py` defines colour palettes; `packs/` contains JSON ecosystem definitions.
- **CLI** – `main.py` glues everything together using Typer.

---

## 🤝 Contribution Guide
We welcome extensions, new shaders, and artistic packs.
1. **Fork** the repository and clone your fork.
2. **Create a branch** for your feature: `git checkout -b feature/awesome‑shader`.
3. **Follow the code style** – see `neonglyph/renderer/utils.py` for logging conventions.
4. **Add tests** in `neonglyph/tests/` (pytest). Run `pytest` before committing.
5. **Update documentation** – add a new entry to `docs/` if you introduce a new concept.
6. **Submit a Pull Request** – describe the artistic intent and how it fits the NeonGlyph Principles.

Please see `CONTRIBUTING.md` for detailed guidelines.

---

## 📄 License
This project is released under the **MIT License**. See the `LICENSE` file for full terms.

---

## 🙏 Acknowledgements
* Inspired by CRT art, VHS glitch aesthetics, and terminal‑based demoscene culture.
* Built with **NumPy**, **OpenCV**, **Typer**, **Rich**, and **Colorama**.
* Special thanks to the community that helped shape the **NeonGlyph Principles**.

---

*Let the terminal dream in light and static.*
