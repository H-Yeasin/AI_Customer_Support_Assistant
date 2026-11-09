# 00 · Project Overview & How to Use These Plans

> **Start every new chat with:**
> "Read `Docs/plans/00-overview.md` and `Docs/plans/week-N-*.md`. Continue from the first unchecked task."
> Load only the overview and the current week's file. Don't load the others, to save tokens.

## Plan files
| File | Focus | Status |
|---|---|---|
| [week-0-setup.md](week-0-setup.md) | Repo, Docker, Postgres+pgvector, FastAPI skeleton, Ollama check | 🟨 |
| [week-1-backend-no-ai.md](week-1-backend-no-ai.md) | Schema, seed data, auth, order and eligibility endpoints, tests, Flutter shell | ⬜ |
| [week-2-assistant-tools.md](week-2-assistant-tools.md) | LLM adapter, tool calling, agent loop, RAG over policies, `/chat` | ⬜ |
| [week-3-controls.md](week-3-controls.md) | Confirmation gate, idempotency, outages and timeouts, streaming, injection tests | ⬜ |
| [week-4-evals-observability.md](week-4-evals-observability.md) | 30 eval cases, eval runner, Langfuse tracing, retrieval metric, model comparison | ⬜ |
| [week-5-differentiator.md](week-5-differentiator.md) | Bangla/Banglish **or** MCP server, plus its evals | ⬜ |
| [week-6-ship-showcase.md](week-6-ship-showcase.md) | Deploy, README, diagram, eval report, demo video, CV/LinkedIn | ⬜ |

Status legend: ⬜ not started · 🟨 in progress · ✅ done. Update this table and the checkboxes in each week's file as you go.

## Goal
An AI customer-support assistant for a **simulated** e-commerce store with three workflows: policy Q&A with citations, order status, and confirmation-gated returns. It's built to (1) learn AI engineering by doing, (2) prepare for interviews, and (3) share on LinkedIn. The full brief is in `Docs/AI_Customer_Support_Assistant_Project.docx.md`.

## Working style: guided build
1. Claude explains the concept briefly and states the task.
2. **You write the code.** Claude reviews it for bugs, security, design and the interview angle.
3. Verify it with tests, curl or the app.
4. Add a dev-log entry in `Docs/dev-log.md` and commit.
5. At the end of each week, draft the LinkedIn post from the dev log.

Claude scaffolds boilerplate only when you ask for it.

## Learner profile
Comfortable with Flutter. FastAPI and Postgres are rusty. New to LLMs. 10–20 hrs/week. Docker and Ollama (`llama3.2:3b`) are installed locally.

## Key decisions
| Area | Decision |
|---|---|
| Main LLM | Ollama `llama3.2:3b` on the Mac host |
| LLM access | Ollama's OpenAI-compatible API (`/v1/chat/completions`) behind a thin `LLMClient` adapter, so swapping models is a config change |
| Comparison model | Week 4: a bigger local model (`qwen2.5:7b` / `llama3.1:8b`) and/or one hosted API |
| Embeddings | Ollama `nomic-embed-text` (768 dims), stored in pgvector |
| Infra | `docker compose`: `db` (pgvector/pgvector:pg16), `api`, and later `langfuse`. Ollama stays on the host and containers reach it at `http://host.docker.internal:11434` |
| Python | 3.12, `uv`, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, pytest |
| Auth | JWT login using seeded fictional customers. `customer_id` **always** comes from the token, never from the model |
| Agent | Hand-written tool loop, no LangChain or agent frameworks |
| Observability | Structured logs until Week 4, then Langfuse |
| Client | Flutter: login, chat, streaming, confirmation dialog |

## Repo layout (target)
```
AI_Customer_Support_Assistant/
├── docker-compose.yml   .env.example   README.md   .gitignore
├── Docs/        plans/  dev-log.md  design-decisions.md  eval-report.md  architecture.png
├── backend/
│   ├── pyproject.toml   Dockerfile   alembic/
│   ├── app/  main.py config.py db.py models.py schemas.py auth.py
│   │        services/ (orders.py returns.py policy.py)
│   │        routers/  (auth.py orders.py returns.py chat.py)
│   │        agent/    (llm_client.py tools.py loop.py prompts.py)
│   ├── seed/  seed.py  policies/{shipping,returns,warranty}.md
│   └── tests/
├── evals/   cases.yaml  run_evals.py  results/
└── mobile/  (Flutter app)
```

## Non-negotiable rules (enforced in code, not in the prompt)
1. A customer can only access their own orders. Another customer's order returns 404.
2. Returns are allowed only within the stated return window and only for returnable items.
3. A return request never triggers a refund.
4. `create_return` needs an explicit user confirmation, and the backend re-checks ownership and eligibility before executing it.
5. Idempotency: retrying the same request returns the existing return instead of creating a duplicate.
6. If a service is down, the assistant says so honestly and never invents a status.

## Commit convention
`feat:`, `fix:`, `chore:`, `test:`, `docs:`. Small commits, at least one per session.
