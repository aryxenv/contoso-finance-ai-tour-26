"""Tests for the Payments domain — realistic processing flow."""

import pytest

# -- Payment method tests --

@pytest.mark.asyncio
async def test_list_payment_methods(client):
    """GET /api/payments/methods returns a list."""
    response = await client.get("/api/payments/methods")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_payment_method(client):
    """POST /api/payments/methods creates and returns a payment method."""
    payload = {"type": "visa", "last_four": "4242"}
    response = await client.post("/api/payments/methods", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "visa"
    assert data["last_four"] == "4242"
    assert "id" in data


# -- Payment creation tests --

@pytest.fixture
async def payment_method_id(client):
    """Helper: create a payment method and return its ID."""
    resp = await client.post("/api/payments/methods", json={"type": "visa", "last_four": "9999"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_payment_returns_pending(client, payment_method_id):
    """POST /api/payments/ creates a payment with status 'pending'."""
    payload = {
        "amount": 100.00,
        "currency": "USD",
        "payment_method_id": payment_method_id,
    }
    response = await client.post("/api/payments/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["amount"] == 100.00
    assert data["currency"] == "USD"
    assert data["reference"].startswith("PAY-")
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_payments(client, payment_method_id):
    """GET /api/payments/ returns paginated list."""
    # Create a payment first
    await client.post("/api/payments/", json={
        "amount": 50.00,
        "currency": "EUR",
        "payment_method_id": payment_method_id,
    })
    response = await client.get("/api/payments/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data


@pytest.mark.asyncio
async def test_get_payment(client, payment_method_id):
    """GET /api/payments/{id} returns a specific payment."""
    create_resp = await client.post("/api/payments/", json={
        "amount": 75.50,
        "currency": "GBP",
        "payment_method_id": payment_method_id,
    })
    payment_id = create_resp.json()["id"]
    response = await client.get(f"/api/payments/{payment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payment_id
    assert data["amount"] == 75.50


@pytest.mark.asyncio
async def test_get_payment_not_found(client):
    """GET /api/payments/{id} returns 404 for non-existent payment."""
    response = await client.get("/api/payments/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


# -- Process payment tests --

@pytest.mark.asyncio
async def test_process_payment_transitions_to_processing(client, payment_method_id):
    """POST /api/payments/{id}/process transitions pending → processing."""
    create_resp = await client.post("/api/payments/", json={
        "amount": 200.00,
        "currency": "USD",
        "payment_method_id": payment_method_id,
    })
    payment_id = create_resp.json()["id"]

    process_resp = await client.post(f"/api/payments/{payment_id}/process")
    assert process_resp.status_code == 200
    data = process_resp.json()
    assert data["status"] == "processing"


@pytest.mark.asyncio
async def test_process_nonexistent_payment_returns_404(client):
    """POST /api/payments/{id}/process returns 404 for non-existent payment."""
    response = await client.post("/api/payments/00000000-0000-0000-0000-000000000000/process")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_process_already_processing_payment_returns_400(client, payment_method_id):
    """POST /api/payments/{id}/process returns 400 if not pending."""
    create_resp = await client.post("/api/payments/", json={
        "amount": 300.00,
        "currency": "USD",
        "payment_method_id": payment_method_id,
    })
    payment_id = create_resp.json()["id"]

    # Process once — should succeed
    await client.post(f"/api/payments/{payment_id}/process")

    # Process again — should fail (status is now 'processing')
    response = await client.post(f"/api/payments/{payment_id}/process")
    assert response.status_code == 400


# -- Status polling tests --

@pytest.mark.asyncio
async def test_get_payment_status(client, payment_method_id):
    """GET /api/payments/{id}/status returns lightweight status."""
    create_resp = await client.post("/api/payments/", json={
        "amount": 150.00,
        "currency": "USD",
        "payment_method_id": payment_method_id,
    })
    payment_id = create_resp.json()["id"]

    response = await client.get(f"/api/payments/{payment_id}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payment_id
    assert data["status"] == "pending"
    assert "reference" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_payment_status_not_found(client):
    """GET /api/payments/{id}/status returns 404 for non-existent payment."""
    response = await client.get("/api/payments/00000000-0000-0000-0000-000000000000/status")
    assert response.status_code == 404


# -- Refund tests --

@pytest.mark.asyncio
async def test_refund_pending_payment_returns_400(client, payment_method_id):
    """POST /api/payments/{id}/refund returns 400 for non-completed payment."""
    create_resp = await client.post("/api/payments/", json={
        "amount": 100.00,
        "currency": "USD",
        "payment_method_id": payment_method_id,
    })
    payment_id = create_resp.json()["id"]

    response = await client.post(f"/api/payments/{payment_id}/refund", json={
        "payment_id": payment_id,
        "reason": "Test refund",
    })
    assert response.status_code == 400
