"""Tests for authentication, including JWT tokens and password hashing/validation."""

import pytest

from contoso_finance.shared.auth.jwt import create_access_token, verify_token
from contoso_finance.shared.auth.password import (
    hash_password,
    validate_password,
    verify_password,
)


def test_create_and_verify_token():
    """Token creation and verification round-trip."""
    token = create_access_token({"sub": "user@example.com"})
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user@example.com"


def test_verify_invalid_token():
    """Invalid token returns None."""
    assert verify_token("invalid.token.value") is None


def test_hash_and_verify_password():
    """Hashing and verification returns True for the original password."""
    password = "Password1"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    """Password verification returns False for a different password."""
    hashed = hash_password("Password1")
    assert verify_password("Different1", hashed) is False


def test_validate_password_valid():
    """A valid password passes validation without raising."""
    validate_password("Password1")


def test_validate_password_too_short():
    """A password shorter than 8 chars raises ValueError."""
    with pytest.raises(ValueError):
        validate_password("abc1")


def test_validate_password_no_letter():
    """A digits-only password raises ValueError."""
    with pytest.raises(ValueError):
        validate_password("12345678")


def test_validate_password_no_number():
    """A letters-only password raises ValueError."""
    with pytest.raises(ValueError):
        validate_password("abcdefgh")
