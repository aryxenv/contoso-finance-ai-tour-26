"""Tests for the settlements domain."""

import pytest


@pytest.mark.asyncio
async def test_list_settlements(client):
    response = await client.get("/api/settlements/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_get_settlement_not_found(client):
    response = await client.get("/api/settlements/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
