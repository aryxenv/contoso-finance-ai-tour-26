"""Tests for JWT authentication."""

from contoso_finance.shared.auth.jwt import create_access_token, verify_token


def test_create_and_verify_token():
    """Token creation and verification round-trip."""
    token = create_access_token({"sub": "user@example.com"})
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user@example.com"


def test_verify_invalid_token():
    """Invalid token returns None."""
    assert verify_token("invalid.token.value") is None
