"""
Supabase authentication utilities for LEXA
Handles user registration, login, and session management with Supabase
"""

import os
import hashlib
import hmac
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from database import SessionLocal
try:
    from sqlalchemy import text
except Exception:  # pragma: no cover - fallback for tests without SQLAlchemy
    def text(query: str):
        return query
from models.user import User
import streamlit as st


class SupabaseAuth:
    """Authentication handler for Supabase integration"""
    
    def __init__(self):
        self.jwt_secret = os.getenv('SUPABASE_JWT_SECRET')
        if not self.jwt_secret:
            raise RuntimeError(
                "SUPABASE_JWT_SECRET environment variable is required"
            )
        self.anon_key = os.getenv('SUPABASE_ANON_KEY', '')
        
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = os.urandom(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                      password.encode('utf-8'), 
                                      salt, 
                                      100000)
        return salt.hex() + ':' + pwdhash.hex()
    
    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify a stored password against provided password"""
        try:
            salt_hex, pwdhash_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            pwdhash = bytes.fromhex(pwdhash_hex)
            
            new_pwdhash = hashlib.pbkdf2_hmac('sha256',
                                            provided_password.encode('utf-8'),
                                            salt,
                                            100000)
            return hmac.compare_digest(pwdhash, new_pwdhash)
        except Exception:
            return False
    
    def create_jwt_token(self, user_id: str, email: str) -> str:
        """Create JWT token for user session"""
        payload = {
            'sub': user_id,
            'email': email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24),
            'role': 'authenticated'
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def register_user(self, email: str, password: str, plan: str = 'free') -> Optional[User]:
        """Register a new user in the database"""
        try:
            with SessionLocal() as session:
                # Check if user already exists
                existing_user = session.execute(
                    text("SELECT id FROM users WHERE email = :email"),
                    {"email": email}
                ).fetchone()
                
                if existing_user:
                    return None  # User already exists
                
                # Hash password
                hashed_password = self.hash_password(password)
                
                # Generate user ID
                import uuid
                user_id = str(uuid.uuid4())
                
                # Insert user
                session.execute(
                    text("""
                        INSERT INTO users (id, email, password_hash, plan, char_usage, credits, created_at)
                        VALUES (:id, :email, :password_hash, :plan, :char_usage, :credits, :created_at)
                    """),
                    {
                        "id": user_id,
                        "email": email,
                        "password_hash": hashed_password,
                        "plan": plan,
                        "char_usage": 0,
                        "credits": 1000,
                        "created_at": datetime.utcnow()
                    }
                )
                session.commit()
                
                # Create User object
                user = User(
                    id=user_id,
                    email=email,
                    plan=plan,
                    char_usage=0,
                    credits=1000
                )
                
                return user
                
        except Exception as e:
            st.error(f"Registration error: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            with SessionLocal() as session:
                # Get user from database
                result = session.execute(
                    text("""
                        SELECT id, email, password_hash, plan, char_usage, credits
                        FROM users WHERE email = :email
                    """),
                    {"email": email}
                ).fetchone()
                
                if not result:
                    return None
                
                # Verify password
                if self.verify_password(result.password_hash, password):
                    # Create User object
                    user = User(
                        id=result.id,
                        email=result.email,
                        plan=result.plan,
                        char_usage=result.char_usage,
                        credits=result.credits
                    )
                    return user
                
                return None
                
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            with SessionLocal() as session:
                result = session.execute(
                    text("""
                        SELECT id, email, plan, char_usage, credits
                        FROM users WHERE id = :user_id
                    """),
                    {"user_id": user_id}
                ).fetchone()
                
                if result:
                    return User(
                        id=result.id,
                        email=result.email,
                        plan=result.plan,
                        char_usage=result.char_usage,
                        credits=result.credits
                    )
                
                return None
                
        except Exception as e:
            st.error(f"Error getting user: {e}")
            return None
    
    def update_user_usage(self, user_id: str, additional_chars: int) -> bool:
        """Update user character usage"""
        try:
            with SessionLocal() as session:
                session.execute(
                    text("""
                        UPDATE users 
                        SET char_usage = char_usage + :additional_chars,
                            updated_at = :updated_at
                        WHERE id = :user_id
                    """),
                    {
                        "user_id": user_id,
                        "additional_chars": additional_chars,
                        "updated_at": datetime.utcnow()
                    }
                )
                session.commit()
                return True
                
        except Exception as e:
            st.error(f"Error updating usage: {e}")
            return False
    
    def check_user_quota(self, user_id: str, text_length: int) -> bool:
        """Check if user has quota for analysis"""
        try:
            with SessionLocal() as session:
                result = session.execute(
                    text("SELECT check_user_quota(:user_id, :text_length)"),
                    {"user_id": user_id, "text_length": text_length}
                ).fetchone()
                
                return bool(result[0]) if result else False
                
        except Exception as e:
            # Fallback to simple check if function doesn't exist
            user = self.get_user_by_id(user_id)
            if user:
                limits = {'free': 10000, 'premium': 100000, 'enterprise': 1000000}
                limit = limits.get(user.plan, 10000)
                return (user.char_usage + text_length) <= limit
            return False


# Global auth instance
supabase_auth = SupabaseAuth()


def get_current_user() -> Optional[User]:
    """Get current authenticated user from session"""
    if 'user_token' in st.session_state:
        payload = supabase_auth.verify_jwt_token(st.session_state.user_token)
        if payload:
            return supabase_auth.get_user_by_id(payload['sub'])
    return None


def login_user(user: User) -> None:
    """Log in user and create session"""
    token = supabase_auth.create_jwt_token(user.id, user.email)
    st.session_state.user_token = token
    st.session_state.user = user


def logout_user() -> None:
    """Log out user and clear session"""
    if 'user_token' in st.session_state:
        del st.session_state.user_token
    if 'user' in st.session_state:
        del st.session_state.user


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return get_current_user() is not None