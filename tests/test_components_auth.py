import importlib
import sys
import types
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import pytest  # noqa: E402

from utils.auth import verify_password  # noqa: E402


@pytest.fixture()
def auth_module(monkeypatch):
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "test-secret")

    if "components.auth" in sys.modules:
        del sys.modules["components.auth"]
    if "utils.supabase_auth" in sys.modules:
        del sys.modules["utils.supabase_auth"]

    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.success = lambda *a, **k: None
    fake_streamlit.error = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)

    fake_sqlalchemy = types.ModuleType("sqlalchemy")
    fake_sqlalchemy.orm = types.ModuleType("sqlalchemy.orm")
    fake_sqlalchemy.orm.Session = object
    monkeypatch.setitem(sys.modules, "sqlalchemy", fake_sqlalchemy)
    monkeypatch.setitem(sys.modules, "sqlalchemy.orm", fake_sqlalchemy.orm)

    fake_users = []

    class FakeUser:
        def __init__(self, email, password_hash, plan="free"):
            self.id = len(fake_users) + 1
            self.email = email
            self.password_hash = password_hash
            self.plan = plan

    fake_models_user = types.ModuleType("models.user")
    fake_models_user.User = FakeUser
    monkeypatch.setitem(sys.modules, "models.user", fake_models_user)

    class FakeQuery:
        def __init__(self, users):
            self._users = users

        def filter_by(self, **kwargs):
            key, value = next(iter(kwargs.items()))
            filtered = [u for u in self._users if getattr(u, key) == value]
            return FakeQuery(filtered)

        def first(self):
            return self._users[0] if self._users else None

    class FakeSession:
        def __init__(self):
            self._users = fake_users

        def query(self, model):
            return FakeQuery(self._users)

        def add(self, obj):
            self._users.append(obj)

        def commit(self):
            pass

        def refresh(self, obj):
            pass

        def close(self):
            pass

    fake_database = types.ModuleType("database")
    fake_database.SessionLocal = lambda: FakeSession()
    monkeypatch.setitem(sys.modules, "database", fake_database)

    auth = importlib.import_module("components.auth")
    return auth


def test_register_and_login_success(auth_module):
    user = auth_module.register_user("user@example.com", "secret")
    assert user is not None
    assert ":" in user.password_hash
    assert verify_password("secret", user.password_hash)
    logged = auth_module.login_user("user@example.com", "secret")
    assert logged is not None
    assert logged.id == user.id


def test_login_wrong_password(auth_module):
    auth_module.register_user("alice@example.com", "password")
    assert auth_module.login_user("alice@example.com", "wrong") is None
