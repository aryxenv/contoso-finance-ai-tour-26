"""Tests for the authentication domain."""

import pytest


async def register_and_login(
    client,
    email: str = "test@example.com",
    password: str = "Password1",
    full_name: str = "Test User",
):
    """Register a user and return auth headers."""
    register_response = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_register_user(client):
    """POST /api/auth/register with valid data creates a user."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "register@test.com",
            "password": "Password1",
            "full_name": "Register User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "register@test.com"
    assert data["full_name"] == "Register User"
    assert data["role"] == "user"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """POST /api/auth/register with an existing email returns 409."""
    payload = {
        "email": "duplicate@test.com",
        "password": "Password1",
        "full_name": "Duplicate User",
    }
    first_response = await client.post("/api/auth/register", json=payload)
    assert first_response.status_code == 201

    second_response = await client.post("/api/auth/register", json=payload)
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password_too_short(client):
    """POST /api/auth/register with too-short password returns 400."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "short-password@test.com",
            "password": "abc1",
            "full_name": "Short Password",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_weak_password_no_number(client):
    """POST /api/auth/register with password missing number returns 400."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "no-number@test.com",
            "password": "abcdefgh",
            "full_name": "No Number",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_weak_password_no_letter(client):
    """POST /api/auth/register with password missing letter returns 400."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "no-letter@test.com",
            "password": "12345678",
            "full_name": "No Letter",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    """POST /api/auth/register with invalid email returns 422."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "not-an-email",
            "password": "Password1",
            "full_name": "Invalid Email",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    """POST /api/auth/login with valid credentials returns bearer token."""
    await client.post(
        "/api/auth/register",
        json={
            "email": "login-success@test.com",
            "password": "Password1",
            "full_name": "Login Success",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "login-success@test.com",
            "password": "Password1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """POST /api/auth/login with wrong password returns 401."""
    await client.post(
        "/api/auth/register",
        json={
            "email": "login-wrong@test.com",
            "password": "Password1",
            "full_name": "Wrong Password",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "login-wrong@test.com",
            "password": "WrongPass1",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    """POST /api/auth/login with unknown email returns 401."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "does-not-exist@test.com",
            "password": "Password1",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client):
    """GET /api/auth/me with a bearer token returns user profile."""
    headers = await register_and_login(
        client,
        email="profile@test.com",
        password="Password1",
        full_name="Profile User",
    )
    response = await client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "profile@test.com"
    assert data["full_name"] == "Profile User"
    assert data["role"] == "user"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_me_no_token(client):
    """GET /api/auth/me without auth header returns 401."""
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_name(client):
    """PATCH /api/auth/me updates the user's full name."""
    headers = await register_and_login(
        client,
        email="update-name@test.com",
        password="Password1",
        full_name="Old Name",
    )
    response = await client.patch(
        "/api/auth/me",
        headers=headers,
        json={"full_name": "New Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "New Name"


@pytest.mark.asyncio
async def test_update_password(client):
    """PATCH /api/auth/me updates password and allows login with new password."""
    email = "update-password@test.com"
    headers = await register_and_login(
        client,
        email=email,
        password="Password1",
        full_name="Password User",
    )

    update_response = await client.patch(
        "/api/auth/me",
        headers=headers,
        json={"password": "NewPassword1", "current_password": "Password1"},
    )
    assert update_response.status_code == 200

    old_login_response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": "Password1"},
    )
    assert old_login_response.status_code == 401

    new_login_response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": "NewPassword1"},
    )
    assert new_login_response.status_code == 200
    assert new_login_response.json()["access_token"]


@pytest.mark.asyncio
async def test_update_password_wrong_current(client):
    """PATCH /api/auth/me with wrong current password returns 400."""
    headers = await register_and_login(
        client,
        email="wrong-current@test.com",
        password="Password1",
        full_name="Wrong Current",
    )
    response = await client.patch(
        "/api/auth/me",
        headers=headers,
        json={"password": "NewPassword1", "current_password": "WrongPassword1"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_password_missing_current(client):
    """PATCH /api/auth/me with new password and no current password returns 400."""
    headers = await register_and_login(
        client,
        email="missing-current@test.com",
        password="Password1",
        full_name="Missing Current",
    )
    response = await client.patch(
        "/api/auth/me",
        headers=headers,
        json={"password": "NewPassword1"},
    )
    assert response.status_code == 400
