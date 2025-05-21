"""Example demonstrating audio-driven fractal generation."""

from __future__ import annotations

import sys

from anus.tools.audio import AudioTool
from anus.tools.fractal import FractalTool


def main() -> None:
    source = sys.argv[1] if len(sys.argv) > 1 else None
    audio = AudioTool()
    fractal = FractalTool()

    audio_result = audio.execute(source=source)
    if not audio_result.is_success():
        print(f"Audio analysis failed: {audio_result.error}")
        return

    features = audio_result.result
    fractal_result = fractal.execute(
        volume=features.get("volume", 0.5),
        frequency=features.get("frequency", 440.0),
    )
    if fractal_result.is_success():
        print(fractal_result.result["fractal"])
    else:
        print(f"Fractal generation failed: {fractal_result.error}")


if __name__ == "__main__":
    main()

