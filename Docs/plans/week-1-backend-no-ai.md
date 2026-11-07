# Week 1 · Backend Without AI (~12–16 hrs)

**Outcome:** every workflow works through Swagger/curl with **no LLM**: login, order lookup with ownership checks, and return eligibility. Tests pass, and a minimal Flutter app logs in and talks to an echo `/chat`.

**Why no AI first:** once an LLM is involved, you can't easily tell whether a bug is in your code or in the model. Make the deterministic part solid first.

---

## Session 1: Database schema + migrations

### Concepts
- **Primary keys / foreign keys / relationships:** `orders.customer_id` references `customers.customer_id`.
- **SQLAlchemy 2.0 ORM:** `DeclarativeBase`, `Mapped[...]`, `mapped_column`, `relationship`.
- **Alembic migrations:** version-controlled schema changes (`revision --autogenerate`, `upgrade head`).
- **Enums and constraints:** an order `status` enum, a `CHECK (quantity > 0)` constraint, and a unique constraint for idempotency.

### Tables
| Table | Fields |
|---|---|
| customers | customer_id (PK, `CUS-001`), name, email, password_hash |
| products | product_id (PK, `PROD-001`), name, category, price, returnable (bool) |
| orders | order_id (PK, `ORD-1001`), customer_id (FK), status (`pending/shipped/delivered/cancelled`), ordered_at, delivered_at (nullable), tracking_reference |
| order_items | item_id (PK), order_id (FK), product_id (FK), quantity |
| returns | return_id (PK, `RET-0001`), order_id (FK), item_id (FK), status (`requested`), reason, idempotency_key (**unique**), created_at |
| policy_chunks | id, doc_name, chunk_index, chunk_text, embedding `vector(768)` (use the `pgvector` Python package) |

### Tasks
- [ ] `app/db.py`: engine, `SessionLocal`, and a `get_db()` dependency
- [ ] `app/models.py`: all 6 tables
- [ ] `alembic init alembic`. Point `env.py` at `settings.database_url` and `Base.metadata`
- [ ] The first migration must run `CREATE EXTENSION IF NOT EXISTS vector` **before** the tables are created (autogenerate won't add this, so add it by hand)
- [ ] `alembic upgrade head`. Inspect the result with `\dt` in psql
- [ ] Commit

### Interview questions
- Why use migrations instead of `Base.metadata.create_all()`?
- Why is the idempotency key a DB unique constraint and not just an `if exists` check in code? (Race conditions.)

---

## Session 2: Seed data + policy documents

### Concepts
- **Deterministic seeds:** the same data on every run (fixed IDs, and dates relative to a fixed "today" or `random.seed(42)`), so evals are reproducible.
- **Exception cases on purpose:** your tests and evals depend on them.

### Tasks
- [ ] `seed/seed.py` (idempotent: truncate, then insert) creating:
  - 20 products, at least 3 with `returnable=False` (e.g. underwear, gift card, perishable)
  - 10 customers with known demo passwords (hashed with `bcrypt`/`passlib`)
  - 50 orders, including **these named cases** (document them in a table in the seed file):
    - `ORD-1007` shipped (from the brief)
    - delivered 3 days ago (eligible)
    - delivered 40 days ago (window expired)
    - cancelled order
    - pending, not yet delivered
    - delivered but containing a non-returnable item
    - 2 orders for the same product owned by different customers (for the auth tests)
- [ ] `seed/policies/shipping.md`, `returns.md` and `warranty.md`, each with concrete rules and numbers: a 14-day return window counted from `delivered_at`, non-returnable categories, the fact that a return ≠ a refund, shipping times, a 12-month warranty
- [ ] Run it: `docker compose exec api uv run python -m seed.seed`
- [ ] Commit

### Interview question
- How do you make an LLM evaluation reproducible?

---

## Session 3: Authentication

### Concepts
- **Password hashing** (bcrypt): never store plain text.
- **JWT:** a signed token with a `sub` (customer_id) and `exp` claim. The server verifies the signature, so it doesn't need to store sessions.
- **`OAuth2PasswordBearer` + `Depends(get_current_customer)`:** every protected endpoint gets the customer from the token.

### Tasks
- [ ] `uv add pyjwt passlib[bcrypt]` (or `bcrypt`)
- [ ] `app/auth.py`: `hash_password`, `verify_password`, `create_token`, `get_current_customer`
- [ ] `POST /auth/login` (email + password) returns `{access_token, token_type}`
- [ ] `GET /me` returns the current customer
- [ ] Add `JWT_SECRET` to `.env.example`
- [ ] Commit

### Interview questions
- Where does `customer_id` come from in your system, and why must it never come from the LLM?
- What's in a JWT? Is the payload encrypted? (No, it's signed. Anyone can read it, but nobody can forge it without the secret.)

---

## Session 4: Order + eligibility endpoints (service layer)

### Concepts
- **Layering:** routers (HTTP) call services (business rules), which call models (DB). In Week 2 the agent tools will call the **same services**.
- **404 vs 403 for another customer's order:** return 404, so the endpoint doesn't reveal that the order exists.
- **Pure functions for rules:** `is_eligible(order, item, product, now) -> (bool, reason)` is easy to unit test.

### Tasks
- [ ] `app/schemas.py`: Pydantic `OrderOut`, `EligibilityRequest`, `EligibilityOut`
- [ ] `services/orders.py`: `get_order_for_customer(db, order_id, customer_id)`, which raises `NotFound` when the order is missing **or** not owned by that customer
- [ ] `services/returns.py`: `check_eligibility(...)` returning `{eligible, reason, policy_ref, deadline}`. Reasons: `not_delivered`, `cancelled`, `window_expired`, `not_returnable`, `already_returned`
- [ ] `GET /orders/{order_id}`
- [ ] `GET /orders` lists my orders (the agent will need this for "return my headphones")
- [ ] `POST /returns/check-eligibility`
- [ ] Commit

---

## Session 5: Tests

### Concepts
- **pytest fixtures:** a test DB (a separate database in the same Postgres instance), the seeded data and a `TestClient`.
- **Test the rules, not just the happy path.**

### Tasks
- [ ] `tests/conftest.py`: test DB, migrations, seed, and a `client` / `auth_headers(customer_id)` fixture
- [ ] Tests:
  - [ ] login succeeds, and a wrong password returns 401
  - [ ] the owner can get `ORD-1007` with the correct status and tracking
  - [ ] customer A requesting customer B's order gets **404**
  - [ ] no token gets 401
  - [ ] eligibility: eligible / window_expired / not_returnable / cancelled / not_delivered
  - [ ] unit tests for the pure `is_eligible` function, including the boundary day (day 14 vs day 15)
- [ ] `uv run pytest` is green. Commit

### Interview question
- How do you test a time-dependent rule? (Inject `now` as a parameter instead of calling `datetime.now()` inside the function.)

---

## Session 6: Minimal Flutter app

### Tasks
- [ ] `flutter create mobile`. Pick a state management approach you know (Riverpod or Provider is fine)
- [ ] Login screen, with the token stored using `flutter_secure_storage`
- [ ] Chat screen: a message list and an input box
- [ ] Backend: `POST /chat` stub (authenticated) that returns `{"reply": "echo: <msg>"}`
- [ ] Configure the base URL (iOS simulator: `localhost`, Android emulator: `10.0.2.2`)
- [ ] Commit

---

## ✅ Week 1 done when
- [ ] The migration and seed run from scratch on a fresh volume
- [ ] All endpoints work in Swagger with a token
- [ ] All tests pass
- [ ] Flutter logs in and gets the echo reply

## 📣 LinkedIn post: "Why I'm building my AI assistant without AI first"
Points to cover: debuggability, rules belong in code, a screenshot of the passing tests, what's coming next week.
