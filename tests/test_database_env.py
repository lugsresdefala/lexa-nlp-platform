import importlib
import sys
import types
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_database_url_env(monkeypatch, tmp_path):
    db_path = tmp_path / "test.db"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("LEXA_DATABASE_URL", url)

    def fake_create_engine(url_val, *, connect_args=None):
        return types.SimpleNamespace(url=url_val, connect_args=connect_args)

    import sqlalchemy

    monkeypatch.setattr(sqlalchemy, "create_engine", fake_create_engine)

    if "database" in sys.modules:
        del sys.modules["database"]
    db = importlib.import_module("database")
    assert str(db.engine.url) == url
