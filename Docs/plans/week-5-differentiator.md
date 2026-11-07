# Week 5 · Differentiator (~10–14 hrs)

**Pick ONE** at the end of Week 4, based on the eval results and your interest. Don't build both.

| Option | Pros | Cons |
|---|---|---|
| **A. Bangla/Banglish** | Realistic for BD e-commerce, rare in portfolios, interesting eval cases | A 3B model may handle Bangla poorly. You may need a bigger model, and that becomes part of the story |
| **B. MCP server** | Shows you know current agent tooling, reuses the same services, quick to demo in Claude Desktop | More common in portfolios |

---

## Option A: Bangla / Banglish support

### Concepts
- **Code-mixed language** (Banglish = Bangla written in Latin letters, mixed with English).
- **Multilingual retrieval:** do the embeddings match "ferot policy ki?" to `returns.md`? Measure it.
- **Choosing a strategy:** (1) ask the model to answer in the user's language, (2) translate the query before retrieval, (3) keep a Bangla version of each policy doc.

### Tasks
- [ ] Collect 15 real-style queries: "amar order kothay?", "ORD-1007 er status ki", "headphone ta ferot dite chai", in both Bangla script and Banglish
- [ ] Measure baseline retrieval and agent performance on them
- [ ] Implement a strategy: language detection, a prompt rule to reply in the user's language, and optionally query normalisation or translation before `search_policy`
- [ ] Optional: Flutter UI string localisation (bn)
- [ ] Add 10+ eval cases (`category: bangla`) and rerun the **full** suite (check for regressions)
- [ ] Commit

---

## Option B: MCP server

### Concepts
- **MCP (Model Context Protocol):** a standard way to expose tools, resources and prompts to any MCP client (Claude Desktop, IDEs and others).
- **Same services, new interface:** this proves the tool interface is stable, as the brief intended.
- **Auth in MCP:** how does the server know the customer? Start with a configured demo customer token, then discuss OAuth as future work.

### Tasks
- [ ] `uv add mcp` (the official Python SDK). Create an `mcp_server/server.py` that exposes `search_policy`, `get_order`, `check_return_eligibility` and `propose_return`
- [ ] Keep the confirmation-gate semantics: the MCP tool proposes, and confirmation is a separate tool that needs the `proposal_id`
- [ ] Expose the policies as MCP **resources**
- [ ] Test with the MCP Inspector, then connect it to an MCP client
- [ ] Add eval or test cases for the MCP tool layer, then rerun the full suite
- [ ] Commit

---

## ✅ Week 5 done when
- [ ] The differentiator works in a demo
- [ ] Its eval cases are added and the full suite is rerun with results committed
- [ ] The design decision is written up in `Docs/design-decisions.md`

## 📣 LinkedIn post: "Teaching my bot Banglish" or "I exposed my support bot as an MCP server"
