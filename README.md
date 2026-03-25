# Contoso Finance

**A modern financial services platform that helps mid‑size enterprises manage payments, cash flow, and financial operations in one unified experience.**

Built for scale, security, and developer velocity, Contoso Finance powers everything from day‑to‑day invoicing to real‑time financial insights — without the complexity of legacy finance systems.

## What Contoso Finance Does

Contoso Finance sits at the center of a company's financial operations, connecting customers, internal teams, and external systems through a single platform.

### Core Capabilities

| Capability | Description |
|---|---|
| **Payments & Invoicing** | Create, send, track, and reconcile invoices and payments across multiple channels. |
| **Financial Operations** | Manage accounts, balances, transactions, and settlements in near real time. |
| **Reporting & Insights** | Give finance teams visibility into cash flow, revenue trends, and operational metrics. |
| **Automation & Integrations** | Connect with internal tools and external partners to automate routine financial workflows. |

## Who It's For

Contoso Finance is designed for organizations that have outgrown spreadsheets and fragmented tools, but don't want to adopt heavyweight enterprise finance software. Typical users include:

- **Finance and accounting teams**
- **Operations and business analysts**
- **Product and engineering teams** integrating financial capabilities
- **Leadership teams** needing reliable financial visibility

## Product Philosophy

| Principle | What It Means |
|---|---|
| ✅ **Simplicity over complexity** | Financial systems should be understandable and predictable, not opaque and fragile. |
| ✅ **Strong domain boundaries** | Each financial capability is clearly defined and owned, reducing coupling and improving reliability. |
| ✅ **Secure by default** | Security, compliance, and auditability are first‑class concerns, not add‑ons. |
| ✅ **Built to evolve** | The platform is designed to grow with the business — from a single product team to a large organization. |

## Platform Structure

At a high level, Contoso Finance consists of:

- A **customer‑facing web application**
- A **single backend platform** that exposes financial capabilities
- **Well‑defined internal domains** such as billing, payments, and reporting
- **Shared components** that ensure consistency across the product

While the platform runs as a single system, it is intentionally structured so individual capabilities can evolve independently over time. This approach allows Contoso Finance to move fast today while staying ready for future scale.

## Architecture

Contoso Finance follows a **modular, domain‑oriented design**:

- **Internally**, the system is composed of distinct business modules that align closely with how finance teams think and work.
- **Externally**, it behaves as a single, cohesive product.

This strikes a balance between the simplicity of a single platform and the clarity and scalability of service‑oriented design.

### Tech Stack

| Layer | Technology |
|---|---|
| Client | React + Vite + TypeScript + SWC |
| Server | Python + FastAPI |
| Database | PostgreSQL (async via SQLAlchemy + asyncpg) |
| Migrations | Alembic |
| Monorepo | Turborepo + npm workspaces |
| Containerization | Docker + docker‑compose |
| CI/CD | GitHub Actions |

### Repository Layout

```
contoso-finance/
├── apps/
│   ├── client/              # React (Vite) web application
│   └── server/              # FastAPI backend
│       └── src/contoso_finance/
│           ├── domains/     # Business domain modules
│           │   ├── billing/
│           │   ├── payments/
│           │   ├── reporting/
│           │   └── settlements/
│           └── shared/      # Cross‑cutting packages
│               ├── auth/
│               ├── database/
│               ├── middleware/
│               └── types/
├── packages/
│   └── shared-types/        # TypeScript API type definitions
├── docker/                  # Dockerfiles + docker‑compose
├── excalidraw/              # Diagrams (Excalidraw sources + exports)
└── skills/                  # Copilot skill files
```

### Domain Modules

Each domain follows a consistent internal structure:

| File | Responsibility |
|---|---|
| `router.py` | FastAPI route definitions |
| `service.py` | Business logic |
| `repository.py` | Data access (async SQLAlchemy) |
| `models.py` | ORM models |
| `schemas.py` | Pydantic request/response schemas |

| Domain | API Prefix | Key Capabilities |
|---|---|---|
| **Billing** | `/api/billing` | Invoice CRUD, send, mark paid |
| **Payments** | `/api/payments` | Process payments, refunds, payment methods |
| **Reporting** | `/api/reporting` | Generate reports, dashboard metrics |
| **Settlements** | `/api/settlements` | Create, reconcile, approve settlements |

## Getting Started

### Prerequisites

- **Node.js** 20+
- **Python** 3.12+
- **uv** (Python package manager) — [install guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker** (for PostgreSQL) — [install guide](https://docs.docker.com/get-docker/)

### Environment Configuration

Contoso Finance uses environment variables for all runtime configuration. A fully documented template is provided in [`.env.example`](.env.example).

```bash
# Copy the template to create your local config
cp .env.example .env
```

The defaults in `.env.example` are configured for local development — no changes are needed to get started. Your `.env` file is gitignored and will never be committed.

**Key variables:**

| Variable | Purpose | Default |
|---|---|---|
| `CONTOSO_DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://…@localhost:5432/contoso_finance` |
| `CONTOSO_JWT_SECRET` | JWT signing key — **must change for production** | `change-me-in-production` |
| `CONTOSO_CORS_ORIGINS` | Allowed CORS origins (JSON array) | `["http://localhost:5173"]` |
| `VITE_API_URL` | Backend URL for the client (build‑time) | `http://localhost:8000` |

All server variables use the `CONTOSO_` prefix and are loaded automatically by [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). See `.env.example` for the complete list with descriptions.

> **Production:** At a minimum, generate a secure `CONTOSO_JWT_SECRET`, set `CONTOSO_CORS_ORIGINS` to your frontend domain(s), and point `CONTOSO_DATABASE_URL` at your production database. See the "Environment‑Specific Notes" section in `.env.example` for details.

### Quick Start (Docker only)

```bash
docker compose -f docker/docker-compose.yml up --build
```

This starts the client (port 3000), server (port 8000), and PostgreSQL — fully containerized.

### Local Development

```bash
# Install dependencies
npm install # root + client + shared-types
cd apps/server && uv venv && uv pip install -r requirements-dev.txt # server

cd .. # Navigate back to root

# Start everything (PostgreSQL + migrations + client + server)
npm run dev
```

`npm run dev` automatically:
1. Starts a PostgreSQL container via Docker
2. Waits for it to be healthy
3. Runs Alembic database migrations
4. Launches the client and server via Turborepo

#### Individual services

```bash
# Client only (http://localhost:5173)
cd apps/client && npm run dev

# Server only (http://localhost:8000)
cd apps/server && uv run uvicorn contoso_finance.main:app --reload --app-dir src

# Turbo only (no Postgres/migrations — assumes DB is already running)
npm run dev:turbo

# Run tests
cd apps/client && npm run test
cd apps/server && uv run pytest tests/ -v

# Database
cd apps/server && npm run db:upgrade      # apply migrations
cd apps/server && npm run db:downgrade    # rollback one migration
cd apps/server && npm run db:reset        # full reset
```

### API Health Check

```bash
curl http://localhost:8000/health
# → {"status": "healthy", "service": "Contoso Finance"}
```

## Why This Repository Exists

This repository represents the core Contoso Finance platform. It is intentionally organized to reflect how modern product teams build and maintain real production systems:

- Clear separation between product areas
- Strong ownership boundaries
- Shared standards and tooling
- A focus on long‑term maintainability

The goal is not just to ship features, but to build a platform that teams can confidently extend and operate.

## Looking Ahead

Contoso Finance is built with the future in mind:

- New financial products can be added without disrupting existing ones
- Domains can be scaled, evolved, or extracted as the business grows
- Integrations and automation capabilities continue to expand

As financial operations become more real‑time, data‑driven, and automated, Contoso Finance aims to be the platform that makes that transition seamless.

## About Contoso

> Contoso is a fictional company used to demonstrate modern software development, platform architecture, and developer tooling in realistic, production‑grade scenarios.

## License

This project is licensed under the [MIT License](LICENSE).
