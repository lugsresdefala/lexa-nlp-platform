import importlib
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture()
def advanced_ui_module(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.markdown = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)

    # Stub plotly modules used by advanced_ui
    fake_plotly = types.ModuleType("plotly")
    fake_go = types.ModuleType("plotly.graph_objects")
    fake_px = types.ModuleType("plotly.express")
    fake_plotly.graph_objects = fake_go
    fake_plotly.express = fake_px
    monkeypatch.setitem(sys.modules, "plotly", fake_plotly)
    monkeypatch.setitem(sys.modules, "plotly.graph_objects", fake_go)
    monkeypatch.setitem(sys.modules, "plotly.express", fake_px)

    advanced_ui = importlib.import_module("components.advanced_ui")
    return advanced_ui


def test_inject_advanced_css_does_not_raise(advanced_ui_module):
    try:
        advanced_ui_module.inject_advanced_css()
    except FileNotFoundError:
        pytest.fail("inject_advanced_css raised FileNotFoundError")
