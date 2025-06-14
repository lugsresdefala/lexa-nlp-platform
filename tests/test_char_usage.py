import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from models.user import User  # noqa: E402
from database import Base  # noqa: E402


def test_char_usage_update():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    user = User()
    user.email = "alice@example.com"
    user.password_hash = "x"
    user.char_usage = 0
    session.add(user)
    session.commit()
    session.refresh(user)

    user.char_usage += 42
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.char_usage == 42
    session.close()
