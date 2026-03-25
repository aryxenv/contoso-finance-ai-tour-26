"""Tests for the billing domain."""

import pytest


@pytest.mark.asyncio
async def test_list_invoices(client):
    """GET /api/billing/invoices returns 200 with paginated response."""
    response = await client.get("/api/billing/invoices")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data


@pytest.mark.asyncio
async def test_create_invoice(client):
    """POST /api/billing/invoices creates and returns an invoice."""
    payload = {
        "customer_name": "Acme Corp",
        "customer_email": "billing@acme.com",
        "currency": "USD",
        "due_date": "2025-12-31",
        "line_items": [
            {"description": "Consulting services", "quantity": 10, "unit_price": 150.00},
            {"description": "Software license", "quantity": 1, "unit_price": 500.00},
        ],
    }
    response = await client.post("/api/billing/invoices", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Acme Corp"
    assert data["status"] == "draft"
    assert data["invoice_number"].startswith("INV-")
    assert len(data["line_items"]) == 2


@pytest.mark.asyncio
async def test_get_invoice_not_found(client):
    """GET /api/billing/invoices/{id} returns 404 for non-existent invoice."""
    response = await client.get("/api/billing/invoices/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
