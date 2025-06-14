from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use SQLite as fallback when DATABASE_URL is not properly configured
DATABASE_URL: str = os.getenv("LEXA_DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///lexa.db"))

# Validate DATABASE_URL format
if DATABASE_URL and not DATABASE_URL.startswith(("postgresql://", "sqlite:///")):
    print(f"Warning: Invalid DATABASE_URL format detected. Using SQLite fallback.")
    DATABASE_URL = "sqlite:///lexa.db"

# Enable multi-threaded access when using SQLite; no extra args for other engines
connect_args: dict[str, object] = (
    {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    """Create all tables registered on the metadata."""
    import models.user  # noqa: F401 – ensures tables are imported before creation

    Base.metadata.create_all(bind=engine)
