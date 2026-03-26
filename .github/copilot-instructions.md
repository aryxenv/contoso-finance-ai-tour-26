# Copilot Instructions — Contoso Finance

## What Is Contoso Finance

Contoso Finance is a modern financial services platform that helps mid-size enterprises manage payments, cash flow, and financial operations in one unified experience. It handles everything from day-to-day invoicing to real-time financial insights — replacing the complexity of legacy finance systems with a product that teams actually want to use.

## Architecture — Modular Monolith in a Monorepo

Contoso Finance is built as a **modular monolith**, deployed as a single system but internally structured around clearly separated business domains. The entire platform lives in this monorepo.

This is a deliberate architectural choice. Rather than starting with distributed microservices (and the operational overhead that comes with them), the platform is organized so that each capability area is self-contained, independently evolvable, and ready to be extracted into its own service if and when the business demands it.

### How the system is structured

- **Client layer** (`apps/client/`) — A React + TypeScript SPA using Fluent UI v9, built with Vite.
- **Server layer** (`apps/server/`) — A Python FastAPI backend with async SQLAlchemy, serving all domain APIs.
- **Domain modules** (`apps/server/src/contoso_finance/domains/`) — Four business domains: **billing**, **payments**, **reporting**, and **settlements**. Each domain owns its logic, data, and boundaries. Domains communicate through explicit contracts, not by reaching into each other's internals.
- **Shared server infrastructure** (`apps/server/src/contoso_finance/shared/`) — Cross-cutting concerns: database base classes, authentication, middleware, and common types.
- **Shared types** (`packages/shared-types/`) — TypeScript type definitions (`@contoso-finance/shared-types`) shared between client and server contracts.
- **Infrastructure** (`docker/`) — Docker Compose with PostgreSQL, server, and client containers. Multi-stage Dockerfiles for production builds.

Externally, Contoso Finance behaves as one product. Internally, it is composed of distinct modules that align with how finance teams think and work.

### Why this approach

| Decision | Rationale |
|---|---|
| **Monorepo** | One repository means shared tooling, unified CI, atomic cross-module changes, and a single source of truth. |
| **Modular monolith** | Gives the clarity and scalability benefits of service-oriented design without the deployment and coordination complexity of microservices. |
| **Strong domain boundaries** | Each module can evolve, scale, or be extracted independently — the architecture grows with the business. |
| **Single deployment** | Simplifies operations today while keeping the door open for future decomposition. |

This architecture is designed to move fast now and stay flexible later.

## Project Structure

```
contoso-finance/
├── apps/
│   ├── client/                    # React + Vite + TypeScript frontend
│   │   ├── src/
│   │   │   ├── api/               # HTTP client (apiClient wrapper)
│   │   │   ├── components/        # Reusable layout components (Header, Sidebar, Layout)
│   │   │   ├── features/          # Feature modules (one directory per domain page)
│   │   │   ├── hooks/             # Custom React hooks
│   │   │   ├── App.tsx            # Root component with FluentProvider + theme
│   │   │   ├── router.tsx         # React Router v7 route definitions
│   │   │   └── theme.ts           # Custom dark theme (GitHub-style)
│   │   └── package.json
│   └── server/                    # Python FastAPI backend
│       ├── src/contoso_finance/
│       │   ├── main.py            # FastAPI app (lifespan, CORS, error handlers, routers)
│       │   ├── config.py          # Pydantic Settings (env-driven configuration)
│       │   ├── domains/           # Business domain modules
│       │   │   ├── billing/       # Invoice management
│       │   │   ├── payments/      # Payment processing
│       │   │   ├── reporting/     # Analytics & dashboards
│       │   │   └── settlements/   # Settlement reconciliation
│       │   └── shared/            # Cross-cutting server infrastructure
│       │       ├── auth/          # Authentication logic
│       │       ├── database/      # SQLAlchemy Base, mixins (UUIDPrimaryKeyMixin, TimestampMixin)
│       │       ├── middleware/    # Error handlers (DomainError, NotFoundError)
│       │       └── types/         # Common enums and types
│       ├── tests/                 # pytest test suite
│       ├── alembic/               # Database migration scripts
│       ├── requirements.txt       # Production dependencies
│       └── requirements-dev.txt   # + dev/test dependencies
├── packages/
│   └── shared-types/              # @contoso-finance/shared-types (TypeScript)
├── docker/
│   ├── docker-compose.yml         # PostgreSQL + server + client
│   ├── Dockerfile.server          # Python 3.12-slim + uv
│   ├── Dockerfile.client          # Multi-stage Node build → nginx
│   └── nginx.conf                 # SPA routing for client
├── scripts/
│   └── dev.js                     # Orchestrated local dev (DB → migrations → turbo dev)
├── skills/                        # Copilot skill files (conventions)
├── turbo.json                     # Turborepo task pipeline
└── package.json                   # Workspace root (npm workspaces)
```

## Expectations for Contributors

### Think in domains

Every change belongs to a domain. Before writing anything, understand which module owns the capability you're working on. Respect boundaries — don't reach across domains to solve a problem that should be solved within one.

### Own your boundaries

If you're building or extending a domain module, you own its contracts, its data, and its behavior. Design interfaces that other modules can depend on without knowing how things work inside yours.

### Keep the monolith modular

The value of this architecture depends on discipline. Shared code should go in shared packages. Domain-specific logic stays in its domain. If something feels like it needs to cut across multiple modules, that's a signal to pause and design the right abstraction — not to take a shortcut.

### Consistency matters

Follow the patterns already established in the codebase. Naming, structure, and conventions exist for a reason — they make the platform predictable for everyone. When in doubt, look at how existing modules are organized and follow the same shape.

### Quality is a default, not a phase

Write code that is clear, tested, and maintainable. This platform is built to last — contributions should reflect that mindset.

## Conventions

### Python tooling — always use `uv`

**All Python package management and script execution in the server (`apps/server/`) MUST use [`uv`](https://docs.astral.sh/uv/).**

- Use `uv pip install` instead of `pip install`.
- Use `uv run` to execute Python tools (`uvicorn`, `pytest`, `ruff`, `alembic`).
- Dependencies are managed via `requirements.txt` and `requirements-dev.txt` — **no `pyproject.toml`** for dependency management.
- Do **not** use raw `pip`, `python -m pip`, or `python -m` commands. Always prefix with `uv`.

```bash
# Install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Run the server
uv run uvicorn contoso_finance.main:app --reload --app-dir src

# Run tests and linting
uv run pytest tests/ -v
uv run ruff check src/ tests/
```

### Frontend UI — Fluent UI v9

**All client UI in `apps/client/` MUST use [Fluent UI v9](https://react.fluentui.dev/) (`@fluentui/react-components`).**

- Use Fluent components (`Button`, `Input`, `Table`, `Card`, `Dialog`, etc.) — not raw HTML elements.
- Use `makeStyles` for custom styling — not CSS files or inline styles.
- Reference theme tokens (`tokens.colorNeutralBackground1`, etc.) for colors — not hardcoded hex values.
- The app uses a **custom GitHub-style dark theme** (`apps/client/src/theme.ts`). All UI must look correct on dark backgrounds.
- Use `@fluentui/react-icons` for icons.
- **Before building custom UI**, consult the `mcp-fluent-ui` MCP server (configured in `.vscode/mcp.json`) to check if a Fluent component exists for the pattern.

See `skills/fluent-ui/SKILL.md` for the full convention reference.

### Domain module structure

Every domain in `apps/server/src/contoso_finance/domains/` follows the same layered structure. When adding a new domain or extending an existing one, replicate this pattern exactly.

```
domains/<name>/
├── __init__.py       # Exports `router` for registration in main.py
├── models.py         # SQLAlchemy ORM models (inherit UUIDPrimaryKeyMixin, TimestampMixin, Base)
├── schemas.py        # Pydantic v2 request/response schemas
├── repository.py     # Data access layer (async SQLAlchemy queries)
├── service.py        # Business logic (calls repository, raises domain errors)
└── router.py         # FastAPI endpoints (calls service, handles HTTP concerns)
```

**Layer responsibilities — never skip a layer:**

| Layer | Owns | Depends on |
|---|---|---|
| **Router** | HTTP methods, status codes, response models, dependency injection | Service |
| **Service** | Business rules, validation logic, error raising | Repository |
| **Repository** | Database queries, ORM operations, pagination | Models |
| **Models** | Table definitions, relationships, constraints | Shared database mixins, shared types |
| **Schemas** | Request/response shapes, field validation | Pydantic BaseModel |

**Router conventions:**

```python
router = APIRouter(prefix="/api/<domain>", tags=["<domain>"])

# Standard CRUD endpoints
@router.get("/<resources>", response_model=<Resource>ListResponse)
@router.get("/<resources>/{resource_id}", response_model=<Resource>Response)
@router.post("/<resources>", response_model=<Resource>Response, status_code=201)
@router.patch("/<resources>/{resource_id}", response_model=<Resource>Response)
@router.delete("/<resources>/{resource_id}", status_code=204)
```

**Schema naming convention:**

- `<Resource>Create` — request body for POST (inherits `BaseModel`)
- `<Resource>Update` — request body for PATCH (all fields optional, inherits `BaseModel`)
- `<Resource>Response` — single-resource response (has `model_config = ConfigDict(from_attributes=True)`)
- `<Resource>ListResponse` — paginated response (inherits `PaginatedResponse[<Resource>Response]`)

### Database & migrations

**PostgreSQL** is the only supported database. All ORM access uses **async SQLAlchemy** with the `asyncpg` driver.

**Model conventions:**

- Every model inherits `UUIDPrimaryKeyMixin`, `TimestampMixin`, and `Base` from `shared.database.base`.
- `UUIDPrimaryKeyMixin` provides `id: UUID` (auto-generated with `uuid4`).
- `TimestampMixin` provides `created_at` and `updated_at` (server-managed, timezone-aware).
- Use `Decimal` with explicit precision for monetary values (e.g., `Numeric(12, 2)`).
- Define relationships with `selectinload` for eager loading in repository queries.

**Migration workflow** (always run from `apps/server/`):

```bash
# Create a new migration after changing models
uv run alembic revision --autogenerate -m "describe the change"

# Apply pending migrations
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1
```

Alembic is configured with `target_metadata = Base.metadata` in `alembic/env.py`. All models must be imported before Alembic can detect changes — ensure new domain models are imported in the alembic env or domain `__init__.py`.

### API design

**Prefix:** All API routes use `/api/<domain>/` as their prefix.

**Pagination:** All list endpoints accept `page` (default 1) and `page_size` (default 20) query parameters. Responses use the `PaginatedResponse` schema:

```json
{
  "items": [...],
  "total": 142,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

**Error handling:** Raise domain-specific exceptions from the service layer — never return raw HTTP errors from services.

- `DomainError(message, status_code=400)` — base exception for business rule violations.
- `NotFoundError(message)` — resource not found (maps to 404).
- Global error handlers in `shared/middleware/error_handler.py` convert these to JSON responses automatically.

**Status codes:**

| Operation | Success code |
|---|---|
| GET (single or list) | 200 |
| POST (create) | 201 |
| PATCH (update) | 200 |
| DELETE | 204 (no body) |
| Action endpoints (e.g., `/send`, `/mark-paid`) | 200 |

### Shared types

The `@contoso-finance/shared-types` package (`packages/shared-types/`) defines TypeScript types shared between client and server contracts. The client imports these for type-safe API interactions.

Key types in `common.ts`:

- `Status` — `'draft' | 'pending' | 'active' | 'completed' | 'cancelled'`
- `CurrencyCode` — `'USD' | 'EUR' | 'GBP'`
- `PaginatedResponse<T>` — generic paginated response shape
- `Money` — `{ amount: number; currency: CurrencyCode }`

When adding a new domain, add its types to `packages/shared-types/src/<domain>.ts` and export from `index.ts`. Keep these types in sync with the corresponding Pydantic schemas on the server.

### Testing

**Backend tests** live in `apps/server/tests/` and mirror the domain structure:

```
tests/
├── conftest.py                   # Shared fixtures (async client, DB session override)
└── domains/
    ├── test_billing.py
    ├── test_payments.py
    ├── test_reporting.py
    └── test_settlements.py
```

**Conventions:**

- Use `pytest` with `pytest-asyncio` (configured with `asyncio_mode = auto` in `pytest.ini`).
- Test through the HTTP layer using the async `httpx.AsyncClient` fixture — not by calling service functions directly. This validates the full request/response cycle.
- The test conftest overrides `get_db` to use a test database session with automatic rollback.
- Every CRUD endpoint must have at least one test per operation (list, get, create, update, delete).
- Name test functions `test_<action>_<resource>` (e.g., `test_create_invoice`, `test_list_payments`).

**Running tests** (from `apps/server/`):

```bash
uv run pytest tests/ -v              # All tests
uv run pytest tests/domains/ -v      # Domain tests only
uv run ruff check src/ tests/        # Linting
```

### Environment & configuration

Application settings are managed through **Pydantic Settings** in `apps/server/src/contoso_finance/config.py`. All settings can be overridden via environment variables with the `CONTOSO_` prefix.

| Setting | Env variable | Default |
|---|---|---|
| `database_url` | `CONTOSO_DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/contoso_finance` |
| `jwt_secret` | `CONTOSO_JWT_SECRET` | `change-me-in-production` |
| `jwt_algorithm` | `CONTOSO_JWT_ALGORITHM` | `HS256` |
| `jwt_expiration_minutes` | `CONTOSO_JWT_EXPIRATION_MINUTES` | `30` |
| `cors_origins` | `CONTOSO_CORS_ORIGINS` | `["http://localhost:5173"]` |
| `debug` | `CONTOSO_DEBUG` | `false` |

Settings are also loaded from a `.env` file in `apps/server/` if present. **Never commit `.env` files or real secrets to the repository.**

The client uses Vite environment variables — `VITE_API_URL` sets the backend base URL (defaults to `http://localhost:8000`).

### Development setup

**Fastest way to start** (requires Docker and Node.js):

```bash
npm install                          # Install all workspace dependencies
cd apps/server && uv pip install -r requirements-dev.txt && cd ../..
npm run dev                          # Starts PostgreSQL, runs migrations, launches client + server
```

`npm run dev` runs `scripts/dev.js`, which orchestrates:
1. Start PostgreSQL via Docker Compose
2. Wait for the database to be healthy
3. Run Alembic migrations (`uv run alembic upgrade head`)
4. Start Turborepo dev (client on `:5173`, server on `:8000`)
5. Clean up containers on exit

**Fully containerized** (no local Node/Python needed):

```bash
docker compose -f docker/docker-compose.yml up --build
# Client → http://localhost:3000  |  Server → http://localhost:8000  |  PostgreSQL → localhost:5432
```

**Health check:**

```bash
curl http://localhost:8000/health
# → {"status": "healthy", "service": "Contoso Finance"}
```

### CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push to `main` and every pull request. **All checks must pass before merging.**

Three parallel jobs:

| Job | What it checks |
|---|---|
| **client** | `npm run lint` → `npm run build` → `npm run test` (Node 20) |
| **server** | `ruff check` → `pytest` with a PostgreSQL service container (Python 3.12 + uv) |
| **shared-types** | `npm run build` — type checking via `tsc --noEmit` (Node 20) |

The server job provisions a real PostgreSQL instance so tests run against the same database engine used in production. Do not write tests that assume SQLite behavior.

### Skill files

This repo uses **skill files** in `skills/` to define detailed conventions for specific workflows. These are the authoritative references:

- **Fluent UI** — `skills/fluent-ui/SKILL.md` defines the component library, dark theme, styling patterns, and MCP server usage. All frontend UI must use Fluent UI v9.
- **Diagrams** — `skills/visuals/SKILL.md` defines the Excalidraw-only diagramming workflow, including dark-mode design rules, the export pipeline, naming conventions, and embedding standards. All diagrams must use Excalidraw.
- **Git workflow** — `skills/git-workflow/SKILL.md` defines branching, conventional commits, atomic commit granularity, and the PR workflow using `gh` CLI. All changes go through feature branches and pull requests — never commit directly to `main`. A generalized version of this skill is also installed globally (`~/.agents/skills/git-workflow/`); the local version takes precedence in this repo and includes Contoso-specific lint commands and paths.
- **Custom agents** — `skills/custom-agents/SKILL.md` defines the template, conventions, and quality bar for authoring GitHub Copilot custom agents (`.agent.md` files in `.github/agents/`). Covers standalone agents, nested orchestrations, tool selection, and Contoso-specific rules. Use this when creating or modifying any agent.

Refer to the relevant skill file before starting work in any of these areas.
