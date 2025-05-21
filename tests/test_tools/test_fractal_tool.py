from anus.tools.fractal import FractalTool


def test_fractal_tool_basic():
    tool = FractalTool()
    result = tool.execute(volume=0.5, frequency=440)
    assert result.is_success()
    fractal = result.result["fractal"]
    assert isinstance(fractal, str)
    assert "*" in fractal

