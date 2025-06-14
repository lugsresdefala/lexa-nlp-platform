import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

import pytest  # noqa: E402

from utils import auth  # noqa: E402
from database import Base  # noqa: E402


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


def test_create_user(db_session):
    user = auth.create_user(
        "alice@example.com", "password123", plan="free", session=db_session
    )
    fetched = auth.get_user("alice@example.com", session=db_session)
    assert fetched is not None
    assert fetched.id == user.id
    assert fetched.email == "alice@example.com"
    assert fetched.plan == "free"


def test_password_hashing_and_verification():
    hashed = auth.hash_password("secret")
    assert auth.verify_password("secret", hashed)
    assert not auth.verify_password("wrong", hashed)


def test_character_quota(db_session):
    user = auth.create_user(
        "bob@example.com", "s3cret", plan="free", session=db_session
    )
    assert auth.check_quota(user.id, 5, session=db_session)
    assert auth.check_quota(user.id, 5, session=db_session)
    assert not auth.check_quota(user.id, user.char_limit, session=db_session)
