# Week 0 · Setup (1–2 sessions, ~4–6 hrs)

**Outcome:** `docker compose up` starts Postgres+pgvector and a FastAPI `/health` endpoint, and a container can reach Ollama on the host.

---

## Session 1: Repo hygiene + Postgres in Docker

### Concepts
- **Repo hygiene:** recruiters look at the repo before the code. Aim for a clean structure and steady, small commits.
- **Docker Compose:** one file describes the whole system.
  - `image`: the packaged software (`pgvector/pgvector:pg16`)
  - `environment`: settings passed into the container (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
  - `ports`: `"5432:5432"` maps host port to container port
  - `volumes`: a named volume `pgdata:/var/lib/postgresql/data`, so data survives `down`
  - `healthcheck`: `pg_isready`, so other services can wait for the DB to be ready
- **Env files:** `.env` holds the real values and stays out of git. `.env.example` is committed with fake values.

### Tasks
- [x] Move the brief into `Docs/`
- [x] Create `Docs/dev-log.md` (template below)
- [x] `.gitignore`: Python (`__pycache__/`, `.venv/`, `.pytest_cache/`), `.env`, `.DS_Store`, Flutter (`build/`, `.dart_tool/`)
- [x] `.env.example` and `.env`
- [x] `docker-compose.yml` with a `db` service using all 5 concepts above
- [x] Enable the pgvector extension and verify it
- [x] First commit: `chore: project setup and postgres via compose`

Dev-log template:
```
## YYYY-MM-DD
- Did:
- Learned:
- Stuck on / surprised by:
```

### Verify
```bash
docker compose up -d
docker compose ps        # STATUS shows (healthy)
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB \
  -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT extversion FROM pg_extension WHERE extname='vector';"
```

### Interview questions (answer them in the dev log)
- What's the difference between `docker compose down` and `down -v`?
- Why does Ollama run on the Mac and not in Docker? (Docker Desktop on macOS can't use the GPU.)
- Why keep secrets out of git, and what would you do if one were leaked?

---

## Session 2: FastAPI skeleton + API container

### Concepts
- **ASGI and uvicorn:** FastAPI is an ASGI app and uvicorn is the server that runs it.
- **Routers:** group endpoints by feature (`routers/orders.py`, …).
- **Dependency injection** (`Depends`): how you'll get a DB session and the current customer into each endpoint.
- **Settings from env:** `pydantic-settings` `BaseSettings` reads `DATABASE_URL`, `OLLAMA_BASE_URL` and so on.
- **`uv`:** a fast Python package and project manager (`uv init`, `uv add`, `uv run`).

### Tasks
- [x] `uv add --dev pytest ruff`
- [x] `app/config.py`: a `Settings` class with `database_url` and `ollama_base_url`
- [x] `app/main.py`: `GET /health` returns `{"status": "ok"}`
- [x] `GET /health/db`: runs `SELECT 1` and reports whether the DB is reachable
- [x] `backend/Dockerfile` (python:3.12-slim, install uv, copy files, run uvicorn on 0.0.0.0:8000)
- [x] Add an `api` service to compose: `depends_on: db: condition: service_healthy`, `extra_hosts: ["host.docker.internal:host-gateway"]`, mount the code and use `--reload` for development
- [x] Commit: `feat: fastapi skeleton with health checks` (app code only; Dockerfile + api service still to do)
- [x] Commit: `feat: dockerize api service`

### Verify
```bash
docker compose up -d --build
curl localhost:8000/health        # {"status":"ok"}
curl localhost:8000/health/db     # DB reachable
open http://localhost:8000/docs   # Swagger UI
```

### Interview questions
- Why use dependency injection instead of a global DB connection?
- Inside a container, why is `localhost` not your Mac?

---

## Session 3 (short): Ollama connectivity

### Concepts
- Ollama serves models over HTTP on port 11434. Its native API is `/api/chat` and its OpenAI-compatible API is `/v1/chat/completions`.
- Embeddings turn text into a vector of numbers. `nomic-embed-text` produces 768 dimensions.

### Tasks
- [x] `ollama pull nomic-embed-text`. Confirm `ollama list` shows `llama3.2:3b` and `nomic-embed-text`
- [x] Call the chat endpoint from the Mac with curl (`/v1/chat/completions`)
- [x] From inside the API container: `docker compose exec api python -c "import httpx; print(httpx.get('http://host.docker.internal:11434/api/tags').json())"`
- [x] Add `OLLAMA_BASE_URL=http://host.docker.internal:11434` to `.env.example`
- [x] Dev log entry, then commit

### Verify
- Both models are listed from inside the container.
- One curl chat completion returns text.

---

## ✅ Week 0 done when
- [] `docker compose up` starts healthy `db` and `api`
- [x] `/health` and `/health/db` return 200
- [x] The container reaches Ollama
- [x] 2–3 commits, and the dev log has entries

**LinkedIn (optional):** none yet. Keep collecting notes for the Week 1 post.
