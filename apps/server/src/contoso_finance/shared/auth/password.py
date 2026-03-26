import bcrypt


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def validate_password(password: str) -> None:
    """Validate password meets security requirements.

    Rules: minimum 8 characters, at least one letter, at least one number.
    Raises ValueError if requirements not met.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(c.isalpha() for c in password):
        raise ValueError("Password must contain at least one letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number")
