import pytest


@pytest.mark.asyncio
async def test_list_reports(client):
    response = await client.get("/api/reporting/reports")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_get_dashboard_metrics(client):
    response = await client.get("/api/reporting/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert "net_income" in data
