import importlib
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture
def metrics_module(monkeypatch):
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


@pytest.fixture
def recommendations_module(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    fake_spacy = types.ModuleType("spacy")
    fake_spacy.tokens = types.SimpleNamespace(Doc=object)
    monkeypatch.setitem(sys.modules, "spacy", fake_spacy)
    monkeypatch.setitem(sys.modules, "numpy", types.ModuleType("numpy"))
    module = importlib.import_module("utils.recommendations")
    return module


class StubToken:
    def __init__(self, text, pos, dep="", lemma=None, is_stop=False, is_punct=False, is_space=False, ancestors=None):
        self.text = text
        self.pos_ = pos
        self.dep_ = dep
        self.lemma_ = lemma if lemma is not None else text
        self.is_stop = is_stop
        self.is_punct = is_punct
        self.is_space = is_space
        self.ancestors = ancestors or []
        self.i = 0


class StubSentence:
    def __init__(self, tokens):
        self.tokens = tokens
    def __iter__(self):
        return iter(self.tokens)
    def __len__(self):
        return len(self.tokens)


class StubDoc:
    def __init__(self, sentences):
        self._sents = [StubSentence(s) for s in sentences]
        self.tokens = [t for s in self._sents for t in s.tokens]
        for idx, t in enumerate(self.tokens):
            t.i = idx
    def __iter__(self):
        return iter(self.tokens)
    def __len__(self):
        return len(self.tokens)
    @property
    def sents(self):
        return [s for s in self._sents]
    @property
    def text(self):
        return " ".join(t.text for t in self.tokens)


def test_calculate_referential_cohesion(metrics_module):
    alice = StubToken("Alice", "PROPN")
    greeted = StubToken("greeted", "VERB")
    him = StubToken("him", "PRON", "dobj", ancestors=[alice])
    bob = StubToken("Bob", "PROPN")
    admired = StubToken("admired", "VERB")
    her = StubToken("her", "PRON", "dobj", ancestors=[bob])
    doc = StubDoc([[alice, greeted, him], [bob, admired, her]])
    score = metrics_module.calculate_referential_cohesion(doc)
    assert score == 80.0


def test_calculate_lexical_cohesion(metrics_module):
    tokens = [
        StubToken("Apple", "NOUN", lemma="apple"),
        StubToken("sells", "VERB", lemma="sell"),
        StubToken("big", "ADJ", lemma="big"),
        StubToken("apples", "NOUN", lemma="apple"),
        StubToken("quickly", "ADV", lemma="quickly"),
    ]
    doc = StubDoc([tokens])
    score = metrics_module.calculate_lexical_cohesion(doc)
    assert score == 100.0


def test_generate_recommendations(monkeypatch, recommendations_module):
    recs = recommendations_module
    monkeypatch.setattr(
        recs,
        "generate_metric_recommendation",
        lambda *a, **k: {"id": "metric", "potential_improvement": 2},
    )
    monkeypatch.setattr(
        recs,
        "generate_general_recommendations",
        lambda *a, **k: [{"id": "general", "potential_improvement": 5}],
    )
    metrics = {
        "overall_score": 60,
        "dimensions": {"coesao": {"referencial": {"score": 50, "expected_range": (70, 90)}}},
    }
    doc = types.SimpleNamespace(text="stub")
    recommendations = recs.generate_recommendations(doc, metrics)
    ids = [r["id"] for r in recommendations]
    assert ids == ["general", "metric"]
