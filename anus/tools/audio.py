"""Audio processing tool for ANUS.

This tool analyzes WAV audio data and returns the relative volume
and an estimated dominant frequency. Microphone capture is attempted
if no file path is provided and the optional ``sounddevice`` package is
available.
"""

from __future__ import annotations

import audioop
import wave
from typing import Any, Dict, Optional

from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult


class AudioTool(BaseTool):
    """Analyze audio input and extract basic features."""

    name = "audio"
    description = "Analyze audio and return volume and dominant frequency"
    parameters = {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "Path to a WAV file. If omitted, tries microphone input.",
            },
            "duration": {
                "type": "number",
                "description": "Recording duration when capturing from microphone",
                "default": 5,
            },
        },
    }

    def execute(
        self,
        source: Optional[str] = None,
        duration: float = 5.0,
        sample_rate: int = 44100,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute the audio analysis."""
        try:
            if source:
                with wave.open(source, "rb") as wf:
                    rate = wf.getframerate()
                    frames = wf.readframes(wf.getnframes())
            else:
                try:
                    import sounddevice as sd  # type: ignore
                    import numpy as np  # type: ignore
                except Exception:
                    return ToolResult.error(
                        self.name,
                        "sounddevice and numpy are required for microphone capture",
                    )
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
                sd.wait()
                frames = (recording[:, 0] * 32767).astype("int16").tobytes()
                rate = sample_rate

            rms = audioop.rms(frames, 2)
            volume = rms / 32768.0

            if len(frames) < 4:
                freq = 0.0
            else:
                samples = [audioop.getsample(frames, 2, i) for i in range(len(frames) // 2)]
                zero_crossings = sum(
                    1 for i in range(1, len(samples)) if (samples[i - 1] < 0) != (samples[i] < 0)
                )
                duration_sec = len(samples) / rate
                freq = zero_crossings / (2 * duration_sec) if duration_sec else 0.0

            result = {"volume": volume, "frequency": freq}
            return ToolResult.success(self.name, result)
        except Exception as exc:  # pragma: no cover - unexpected errors
            return ToolResult.error(self.name, str(exc))
