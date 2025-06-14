import importlib
import sys
import types
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import pytest  # noqa: E402


@pytest.fixture()
def layout_module(monkeypatch):
    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.markdown = lambda *a, **k: None
    fake_streamlit.image = lambda *a, **k: None
    fake_streamlit.columns = lambda *args, **kwargs: [
        types.SimpleNamespace(),
        types.SimpleNamespace(),
    ]
    fake_streamlit.title = lambda *a, **k: None
    fake_streamlit.caption = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)

    layout = importlib.import_module("components.layout")
    return layout


def test_render_header_returns_markup(layout_module):
    html = layout_module.render_header("T", "S")
    assert 'class="header"' in html
    assert "T" in html
    assert "S" in html


def test_render_footer_returns_markup(layout_module):
    html = layout_module.render_footer()
    assert "class='footer'" in html or 'class="footer"' in html
