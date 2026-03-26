"""Domain module registry — registers all domain routers with the FastAPI app."""

from fastapi import FastAPI


def register_routers(app: FastAPI) -> None:
    """Register all domain routers.

    Each domain module exposes a `router` attribute in its __init__.py.
    Add new domains here as they are created.
    """
    from contoso_finance.domains.billing import router as billing_router

    app.include_router(billing_router)

    from contoso_finance.domains.auth import router as auth_router

    app.include_router(auth_router)

    from contoso_finance.domains.reporting import router as reporting_router

    app.include_router(reporting_router)

    from contoso_finance.domains.payments import router as payments_router

    app.include_router(payments_router)

    from contoso_finance.domains.settlements import router as settlements_router

    app.include_router(settlements_router)
