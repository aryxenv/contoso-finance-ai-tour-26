import pytest


@pytest.mark.asyncio
async def test_list_payments(client):
    response = await client.get("/api/payments/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_list_payment_methods(client):
    response = await client.get("/api/payments/methods")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
