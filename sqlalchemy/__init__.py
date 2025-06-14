"""Lightweight in‑memory stub emulating a minimal subset of SQLAlchemy.
This file removes merge‑conflict artefacts and harmonises class naming.
It is **not** a drop‑in replacement for SQLAlchemy; it only implements the
behaviour required by LEXA tests.
"""

from types import SimpleNamespace
import sys
from typing import Any, Dict, List, Type


# ---------------------------------------------------------------------------
# Column & Field Types
# ---------------------------------------------------------------------------
class Column:  # noqa: D101 – simplified stub
    def __init__(
        self,
        _type: Type[Any],
        *,
        primary_key: bool = False,
        index: bool = False,
        unique: bool = False,
        nullable: bool = True,
        default: Any | None = None,
    ) -> None:
        self.type = _type
        self.primary_key = primary_key
        self.index = index
        self.unique = unique
        self.nullable = nullable
        self.default = default


class Integer:  # noqa: D101
    pass


class String:  # noqa: D101
    pass


class DateTime:  # noqa: D101
    pass


def text(query: str) -> str:  # noqa: D401
    """Return the query string itself."""
    return query


# Relationship placeholder ---------------------------------------------------


def relationship(*_: Any, **__: Any) -> None:  # noqa: D401, D403 – stub only
    """Return ``None`` – relationship handling is out of scope for the stub."""
    return None


# ---------------------------------------------------------------------------
# Declarative Base & Metadata
# ---------------------------------------------------------------------------
class _Meta:  # noqa: D101
    def create_all(self, bind: Any | None = None) -> None:  # noqa: ANN001
        """Pretend to create all tables using the provided bind."""
        del bind  # not implemented – present for API compatibility


class Base:  # noqa: D101
    metadata = _Meta()

    def __init__(self, **kwargs: Any) -> None:  # noqa: D401, ANN001
        # Populate mapped columns with provided or default values
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, Column):
                value = kwargs.pop(name, attr.default)
                setattr(self, name, value)
        # Handle any additional kwargs (useful for non‑mapped fields in tests)
        for key, value in kwargs.items():
            setattr(self, key, value)


def declarative_base() -> Type[Base]:  # noqa: D401
    """Return the declarative :class:`~Base` stub."""
    return Base


# ---------------------------------------------------------------------------
# Engine & Session
# ---------------------------------------------------------------------------


def create_engine(
    url: str, *, connect_args: Dict[str, Any] | None = None
) -> SimpleNamespace:  # noqa: D401
    """Return a dummy engine namespace (URL is ignored)."""
    del url, connect_args
    return SimpleNamespace()


class Session:  # noqa: D101
    def __init__(self, *, bind: Any | None = None):  # noqa: ANN001
        self.bind = bind
        self._objects: List[Any] = []

    # CRUD helpers -----------------------------------------------------------
    def add(self, obj: Any) -> None:  # noqa: D401, ANN001
        self._objects.append(obj)

    def commit(self) -> None:  # noqa: D401
        # No‑op for in‑memory store
        return None

    def refresh(self, obj: Any) -> None:  # noqa: D401, ANN001
        # No‑op; real SQLAlchemy would issue a SELECT here
        return None

    def close(self) -> None:  # noqa: D401
        self._objects.clear()

    def get(self, model: Type[Any], ident: Any):  # noqa: D401, ANN001
        """Return the first stored object of ``model`` with ``id`` equal to ``ident``."""
        for obj in self._objects:
            if isinstance(obj, model) and getattr(obj, "id", None) == ident:
                return obj
        return None

    # Query helper -----------------------------------------------------------
    def query(self, model: Type[Any]):  # noqa: D401, ANN001
        objs = [o for o in self._objects if isinstance(o, model)]

        class Query:  # noqa: D106 – internal helper class
            def __init__(self, _objs: List[Any]):
                self._objs = _objs

            def filter_by(self, **kwargs: Any):  # noqa: D401, ANN001
                filtered = [
                    o
                    for o in self._objs
                    if all(getattr(o, k, None) == v for k, v in kwargs.items())
                ]
                return Query(filtered)

            def first(self):  # noqa: D401
                return self._objs[0] if self._objs else None

            def get(self, ident: Any):  # noqa: D401, ANN001
                for o in self._objs:
                    if getattr(o, "id", None) == ident:
                        return o
                return None

        return Query(objs)


# ---------------------------------------------------------------------------
# Session factory & orm namespace
# ---------------------------------------------------------------------------


def sessionmaker(
    *, autocommit: bool = False, autoflush: bool = False, bind: Any | None = None
):  # noqa: D401, ANN001
    del autocommit, autoflush

    def _factory() -> Session:  # noqa: D401
        return Session(bind=bind)

    return _factory


# Expose an "orm" submodule with common helpers to mimic SQLAlchemy import path
orm = SimpleNamespace(
    sessionmaker=sessionmaker,
    declarative_base=declarative_base,
    relationship=relationship,
    Session=Session,
)

# Make it importable as ``import db_stub.orm``
sys.modules[__name__ + ".orm"] = orm
