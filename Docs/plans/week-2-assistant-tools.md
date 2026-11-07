# Week 2 · Assistant and Tools (~12–16 hrs)

**Outcome:** `POST /chat` runs a single-agent tool-calling loop on `llama3.2:3b`. All three workflows work end-to-end from Swagger, and policy answers cite the source document.

**Core idea for interviews:** the model **proposes** a tool call, your code **validates and executes** it, and the result goes back to the model. The model never touches the DB.

---

## Session 1: LLM client adapter

### Concepts
- **Chat messages and roles:** `system`, `user`, `assistant`, `tool`.
- **Parameters:** `temperature` (use 0–0.2 for support work, since it should be predictable), `max_tokens`.
- **Token usage:** `prompt_tokens` and `completion_tokens`, which drive cost and latency.
- **Adapter pattern:** one interface, many providers. This makes the Week-4 comparison easy.

### Tasks
- [ ] `uv add openai`. The OpenAI SDK can talk to Ollama at `base_url=f"{OLLAMA_BASE_URL}/v1"` with `api_key="ollama"`
- [ ] `agent/llm_client.py`: `class LLMClient: def chat(messages, tools=None) -> LLMResponse`, where `LLMResponse` has `content`, `tool_calls`, `usage` and `latency_ms`
- [ ] `LLM_MODEL=llama3.2:3b` in config
- [ ] A small script, `scripts/try_llm.py`, that sends "hello" and prints the response and usage
- [ ] Commit

### Interview question
- Why wrap the SDK in your own client instead of calling it everywhere?

---

## Session 2: Tool definitions + dispatcher

### Concepts
- **Tool schema:** name, description and JSON-Schema parameters. **The description is a prompt**, so write it precisely.
- **Narrow tools:** small, single-purpose tools are easier for a 3B model to use correctly.
- **Server-side context injection:** the dispatcher adds `customer_id` from the session, and that field doesn't appear in the schema at all.
- **Validate tool arguments** with Pydantic. Bad arguments get an error result back to the model, not a crash.

### Tools
| Tool | Args (from the model) | Calls |
|---|---|---|
| `search_policy` | `query: str` | `services/policy.search(query, k=3)` |
| `list_my_orders` | (none) | `services/orders.list_for_customer` |
| `get_order` | `order_id: str` | `services/orders.get_order_for_customer` |
| `check_return_eligibility` | `order_id, item_id` | `services/returns.check_eligibility` |
| `create_return` | `order_id, item_id, reason` | **Week 3: proposal only.** In Week 2, leave it stubbed or out |

### Tasks
- [ ] `agent/tools.py`: `TOOL_SCHEMAS` (list) and `execute_tool(name, args_json, ctx) -> dict`
- [ ] `ctx` = `{db, customer_id}`. An unknown tool name or invalid args return `{"error": ...}`
- [ ] Unit test the dispatcher without any LLM involved
- [ ] Commit

---

## Session 3: Agent loop

### Concepts
- **The loop:** send the messages and tools, then
  - if the model returns tool calls: execute each one, append a `tool` message, and loop again
  - otherwise: return the final answer
- **Guards:** `MAX_STEPS` (e.g. 5) to prevent infinite loops, and a cap on tool result size.
- **System prompt:** role, the rules (only use tool data, never invent an order status, cite policy docs), and a refusal style for off-topic requests.

### Tasks
- [ ] `agent/prompts.py`: a versioned `SYSTEM_PROMPT_V1`
- [ ] `agent/loop.py`: `run_agent(messages, ctx) -> AgentResult(reply, tool_trace[], usage)`
- [ ] Log each step as JSON: tool name, arguments, result summary, latency
- [ ] Commit

### Expect with a 3B model (write these in the dev log, since they're post material)
- Malformed tool-call JSON, calling the wrong tool, or answering without calling any tool
- Mitigations: clearer tool descriptions, fewer tools, few-shot examples in the system prompt, temperature 0, and a retry when JSON parsing fails

---

## Session 4: RAG over policies

### Concepts
- **Chunking:** split the policies by heading or paragraph (~200–400 tokens) and keep `doc_name` with each chunk.
- **Embeddings:** `nomic-embed-text` via Ollama `/api/embed`. Note that nomic expects the prefixes `search_document: ` and `search_query: `.
- **Vector search:** pgvector `embedding <=> query_vec` (cosine distance), `ORDER BY ... LIMIT k`.
- **Grounding and citation:** the tool returns `{doc_name, chunk_text, score}` and the prompt requires a "Source: returns.md" line.

### Tasks
- [ ] `services/policy.py`: `ingest_policies()` (chunk, embed, upsert) and `search(query, k)`
- [ ] Run ingest as part of the seed step
- [ ] Optional: an HNSW index (`USING hnsw (embedding vector_cosine_ops)`). For around 30 chunks it doesn't matter, but know why it exists
- [ ] Manually test 5 policy questions and check that the right doc comes back first
- [ ] Commit

### Interview questions
- What is RAG, and why use it instead of putting all the policies in the prompt? (At this scale, putting them all in the prompt would actually work. Be honest about that trade-off.)
- What is cosine similarity?

---

## Session 5: `/chat` endpoint + conversation state

### Tasks
- [ ] A `conversations` and `messages` table (or an in-memory dict to start, then move it to the DB)
- [ ] `POST /chat {conversation_id?, message}` returns `{conversation_id, reply, tool_trace}`
- [ ] Hook up the Flutter chat to the real `/chat`
- [ ] Try the workflows:
  - [ ] "What is your return policy?" gets an answer citing `returns.md`
  - [ ] "Where is ORD-1007?" (as its owner) gives the status and tracking
  - [ ] "Can I return my headphones?" lists orders, checks eligibility and explains the result
- [ ] Commit

---

## ✅ Week 2 done when
- [ ] All 3 workflows work in Swagger and in Flutter
- [ ] The tool trace shows the correct tools and arguments
- [ ] Policy answers cite their source
- [ ] The dev log records where the 3B model failed

## 📣 LinkedIn post: "How function calling works: the model proposes, my code executes"
Include a sequence diagram (User → API → LLM → tool → DB → LLM → User) and one real trace.
