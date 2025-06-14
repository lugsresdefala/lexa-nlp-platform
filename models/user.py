from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from config import PLANS

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan = Column(String, default="free")
    char_usage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.__dict__.setdefault("char_usage", 0)

    @property
    def char_limit(self) -> int:
        """Return the monthly character limit based on the user's plan."""
        return PLANS.get(self.plan, 0)

    def has_quota(self, additional_chars: int = 0) -> bool:
        """Check if the user has remaining quota for additional characters."""
        limit = self.char_limit
        if not limit:
            return False
        return (self.char_usage + additional_chars) <= limit
