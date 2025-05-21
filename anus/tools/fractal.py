"""Fractal generation tool for ANUS.

Produces a simple ASCII fractal tree whose depth and branch angle
are influenced by audio features. This avoids external dependencies
so it can run in minimal environments.
"""

from __future__ import annotations

from typing import Any, List

from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult


class FractalTool(BaseTool):
    """Generate ASCII fractal trees."""

    name = "fractal"
    description = "Generate an ASCII fractal tree modulated by audio features"
    parameters = {
        "type": "object",
        "properties": {
            "volume": {"type": "number", "description": "Relative volume"},
            "frequency": {"type": "number", "description": "Dominant frequency"},
            "depth": {"type": "integer", "description": "Override recursion depth"},
        },
    }

    def execute(
        self,
        volume: float = 0.5,
        frequency: float = 440.0,
        depth: int | None = None,
        **kwargs: Any,
    ) -> ToolResult:
        """Generate the fractal as text."""
        try:
            if depth is None:
                depth = max(1, int(volume * 10))
            depth = min(depth, 6)
            lines = self._build_tree(depth)
            fractal = "\n".join(lines)
            meta = {"volume": volume, "frequency": frequency, "depth": depth}
            return ToolResult.success(self.name, {"fractal": fractal, **meta})
        except Exception as exc:  # pragma: no cover - unexpected errors
            return ToolResult.error(self.name, str(exc))

    def _build_tree(self, depth: int) -> List[str]:
        if depth == 0:
            return ["*"]
        prev = self._build_tree(depth - 1)
        width = len(prev[-1])
        top = [" " * width + line + " " * width for line in prev]
        trunk = "/" + " " * width + "\\"
        bottom = [line + " " + line for line in prev]
        return top + [trunk] + bottom

