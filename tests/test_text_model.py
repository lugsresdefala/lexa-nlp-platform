import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from models.text import Text, save_text  # noqa: E402


def test_save_text(tmp_path, monkeypatch):
    path = tmp_path / "texts.json"
    text = Text(
        id="1",
        user_id="u1",
        content="hello",
        language="en",
        domain="Test",
        created_at="now",
    )
    save_text(text, path=str(path))
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["id"] == "1"
    assert data[0]["user_id"] == "u1"
    assert data[0]["content"] == "hello"
