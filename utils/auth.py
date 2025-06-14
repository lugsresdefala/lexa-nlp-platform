import hashlib
import os
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    """Return a salted password hash suitable for storage."""
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + ":" + hashed.hex()


def verify_password(password: str, stored: str) -> bool:
    """Verify a password against the stored hash."""
    try:
        salt_hex, hash_hex = stored.split(":")
    except ValueError:
        return False
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 100000
    )
    return hashed.hex() == hash_hex


def create_user(
    email: str,
    password: str,
    *,
    plan: str = "free",
    session: Session | None = None,
) -> User:
    """Create a new user and return the model instance."""
    close = False
    if session is None:
        session = SessionLocal()
        close = True
    try:
        password_hash = hash_password(password)
        user = User(email=email, password_hash=password_hash, plan=plan)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        if close:
            session.close()


def get_user(email: str, session: Session | None = None) -> User | None:
    """Retrieve a user by email."""
    close = False
    if session is None:
        session = SessionLocal()
        close = True
    try:
        return session.query(User).filter_by(email=email).first()
    finally:
        if close:
            session.close()


def check_quota(user_id: int, new_chars: int, session: Session | None = None) -> bool:
    """Return True and update usage if the user has enough remaining characters."""
    close = False
    if session is None:
        session = SessionLocal()
        close = True
    try:
        user = session.get(User, user_id)
        if user is None or not user.has_quota(new_chars):
            return False
        user.char_usage += new_chars
        session.commit()
        return True
    finally:
        if close:
            session.close()
