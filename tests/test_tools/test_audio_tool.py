import wave
import struct

from anus.tools.audio import AudioTool


def test_audio_tool_file(tmp_path):
    sample_rate = 8000
    samples = [0] * sample_rate  # 1 second of silence
    path = tmp_path / "test.wav"
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(struct.pack("<h", s) for s in samples))

    tool = AudioTool()
    result = tool.execute(source=str(path))
    assert result.is_success()
    assert "volume" in result.result
    assert "frequency" in result.result

