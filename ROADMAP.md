# Roadmap

## Phases

Work the issues in phase order. Issues within a phase are independent — do them in parallel or any order, unless noted otherwise.

### Phase 1 — Core Backend

Initial Alembic migration is complete. These are all parallel.

| Issue | What                                                 |
| ----- | ---------------------------------------------------- |
| #22   | User registration & session management               |
| #3    | Realistic payment processing flow                    |
| #5    | Real settlement amounts from payment data            |
| #7    | Real reporting data aggregation                      |
| #2    | Expand server test coverage beyond placeholder stubs |

### Phase 2 — Auth Completion & Cross-Domain

Serial chains from Phase 1.

| Issue | What                                          | Depends on |
| ----- | --------------------------------------------- | ---------- |
| #4    | Wire JWT authentication to all endpoints      | #22        |
| #6    | Cross-domain validation between modules       | #3, #5     |
| #10   | Database seed script for development          | #3, #5, #7 |
| #21   | Harden JWT configuration & add refresh tokens | #4         |
| #20   | API rate limiting middleware                  | #4         |

### Phase 3 — Frontend

Can overlap with Phase 2 — APIs work today, backend improvements just make data more realistic.

**Do #8 first.** Prettier formatting must land before any other frontend PR to avoid merge conflicts across every file.

| Issue | What                                         | Better after          |
| ----- | -------------------------------------------- | --------------------- |
| #8    | Set up Prettier for consistent formatting    | — (**do this first**) |
| #14   | Build Billing page with invoice management   | — (API is complete)   |
| #11   | Build Payments page with transaction history | #3                    |
| #12   | Build Dashboard page with real-time metrics  | #7                    |
| #15   | Build Reporting page with charts & reports   | #7                    |
| #13   | Build Settlements page with workflow mgmt    | #5                    |

### Phase 4 — Quality & Docs

After features are built.

| Issue | What                                   |
| ----- | -------------------------------------- |
| #1    | End-to-end testing with Playwright     |
| #16   | CONTRIBUTING.md guide                  |
| #9    | Architecture diagrams using Excalidraw |

### Phase 5 — Production Readiness

| Issue | What                                   | Depends on |
| ----- | -------------------------------------- | ---------- |
| #17   | Harden nginx configuration             | —          |
| #18   | Docker image build & push to CI        | —          |
| #19   | Staging/production deployment workflow | #18        |

## Dependencies

**Hard** — will break or require rework if ignored:

```
#22 → #4
#4 → #21, #20
#3 + #5 → #6
#3 + #5 + #7 → #10
#18 → #19
#8 → all frontend pages (#14, #11, #12, #15, #13)
```

**Soft** — better in order, won't break if skipped:

```
#3 → #11 (payments page)
#5 → #13 (settlements page)
#7 → #12, #15 (dashboard, reporting pages)
```
