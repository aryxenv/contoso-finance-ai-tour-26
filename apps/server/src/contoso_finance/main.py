"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contoso_finance.config import settings
from contoso_finance.domains import register_routers
from contoso_finance.shared.middleware.error_handler import register_error_handlers

API_DESCRIPTION = """
## Contoso Finance API

A modern financial services platform for mid-size enterprises to manage payments,
cash flow, and financial operations in one unified experience.

### Domains

| Domain | Description |
|--------|-------------|
| **Billing** | Invoice lifecycle management — create, send, and track invoices |
| **Payments** | Payment processing, payment methods, and refunds |
| **Reporting** | Financial analytics, report generation, and dashboard metrics |
| **Settlements** | Settlement reconciliation, approval, and completion workflows |

### Authentication

All endpoints require a valid JWT bearer token unless otherwise noted.
Pass the token in the `Authorization` header as `Bearer <token>`.
"""

OPENAPI_TAGS = [
    {
        "name": "auth",
        "description": "Authentication and user profile management — register, login, and manage current user details.",
    },
    {
        "name": "billing",
        "description": "Invoice management — create, update, send, and track invoices through their lifecycle.",
    },
    {
        "name": "payments",
        "description": "Payment processing — manage payment methods, process payments, and handle refunds.",
    },
    {
        "name": "reporting",
        "description": "Financial reporting — generate reports, view analytics, and access dashboard metrics.",
    },
    {
        "name": "settlements",
        "description": "Settlement reconciliation — batch payments into settlements, reconcile, approve, and complete.",
    },
    {
        "name": "health",
        "description": "Operational health checks.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    yield


app = FastAPI(
    title=settings.app_name,
    description=API_DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=OPENAPI_TAGS,
    contact={
        "name": "Contoso Finance Engineering",
        "url": "https://github.com/aryxenv/contoso-finance",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/aryxenv/contoso-finance/blob/main/LICENSE",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handlers
register_error_handlers(app)

# Domain routers
register_routers(app)


@app.get("/health", tags=["health"])
async def health_check():
    """Check whether the API is up and responding."""
    return {"status": "healthy", "service": settings.app_name}
