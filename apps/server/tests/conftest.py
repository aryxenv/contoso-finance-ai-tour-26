"""Shared test fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import contoso_finance.domains.billing.models  # noqa: F401
import contoso_finance.domains.payments.models  # noqa: F401
import contoso_finance.domains.reporting.models  # noqa: F401
import contoso_finance.domains.settlements.models  # noqa: F401
from contoso_finance.config import settings
from contoso_finance.main import app
from contoso_finance.shared.database.base import Base
from contoso_finance.shared.database.session import get_db

# Use instant processing in tests to avoid slow background-task delays
settings.payment_processing_delay_seconds = 0
settings.payment_failure_rate = 0.0


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables before tests and drop them after."""
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client():
    """Async HTTP test client for the FastAPI app."""
    engine = create_async_engine(settings.database_url)
    test_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with test_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    transport= ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()
