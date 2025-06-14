import importlib
import sys
import types
from pathlib import Path

import pytest


def test_load_css_does_not_raise(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.markdown = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)

    styling = importlib.import_module("utils.styling")
    try:
        styling.load_css()
    except FileNotFoundError:
        pytest.fail("load_css raised FileNotFoundError")
