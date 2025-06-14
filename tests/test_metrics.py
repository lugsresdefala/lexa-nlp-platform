import importlib
import sys
import types
from pathlib import Path
import pytest


@pytest.fixture
def metrics_module(monkeypatch):
    # Provide dummy modules for heavy dependencies
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    fake_spacy = types.ModuleType("spacy")
    fake_spacy.tokens = types.SimpleNamespace(Doc=object)
    monkeypatch.setitem(sys.modules, "spacy", fake_spacy)
    monkeypatch.setitem(sys.modules, "numpy", types.ModuleType("numpy"))
    fake_sklearn = types.ModuleType("sklearn")
    fake_sk_metrics = types.ModuleType("sklearn.metrics")
    fake_sk_metrics.pairwise = None
    fake_sklearn.metrics = fake_sk_metrics
    monkeypatch.setitem(sys.modules, "sklearn", fake_sklearn)
    monkeypatch.setitem(sys.modules, "sklearn.metrics", fake_sk_metrics)

    metrics = importlib.import_module("utils.metrics")
    return metrics


def test_get_expected_range_academico(metrics_module):
    func = metrics_module.get_expected_range
    assert func(
        "coesao", "referencial", "Acad\u00eamico", "Artigo Cient\u00edfico"
    ) == (65, 85)


def test_get_expected_range_literario_complexidade(metrics_module):
    func = metrics_module.get_expected_range
    assert func("complexidade", "lexical", "Liter\u00e1rio", "Narrativa") == (60, 85)


def test_calculate_percentile(monkeypatch, metrics_module):
    metrics = metrics_module
    # Mock reference corpus stats
    monkeypatch.setitem(
        metrics.REFERENCE_CORPUS_STATS, "overall", {"Test": {"mean": 50, "std_dev": 5}}
    )
    # Mock scipy.stats.norm.cdf
    fake_stats = types.SimpleNamespace(norm=types.SimpleNamespace(cdf=lambda z: z))
    fake_scipy = types.ModuleType("scipy")
    fake_scipy.stats = fake_stats
    monkeypatch.setitem(sys.modules, "scipy", fake_scipy)
    monkeypatch.setitem(sys.modules, "scipy.stats", fake_stats)
    percentile = metrics.calculate_percentile(55, "Test")
    assert percentile == 100.0
