# Week 6 · Ship and Showcase (~10–14 hrs)

**Outcome:** a reproducible repo, a public demo (or a solid recorded one), an eval report, a demo video, posts, and an updated CV and LinkedIn.

---

## Session 1: Reproducibility + deploy

### Tasks
- [ ] Fresh-clone test on a clean folder: `cp .env.example .env && docker compose up -d && make seed` works with no manual steps
- [ ] A `Makefile` (or `justfile`) with `up`, `seed`, `test`, `eval` and `down`
- [ ] Choose how to deploy:
  - **Option 1 (simplest, free):** a recorded demo plus local run instructions. Ollama can't run on a cheap host
  - **Option 2:** deploy the API and DB on a VPS or Fly.io/Railway with a **hosted** small LLM for the public demo, with rate limiting and fictional accounts only
  - Flutter: build for web (`flutter build web`) or ship an APK release
- [ ] A visible "SIMULATED STORE · fictional data" banner in the app
- [ ] Commit

---

## Session 2: README + architecture diagram

### README sections
1. What it is, in one paragraph, plus a GIF
2. The simulated-business disclaimer
3. An architecture diagram
4. How tool calling works here (model proposes, code executes)
5. Safety rules and how each one is enforced in code
6. Eval results summary with a link to the full report
7. Model comparison table
8. Trace screenshots
9. Run it locally (3 commands)
10. Known limitations and future work (a Shopify adapter, OAuth for MCP, and so on)

### Tasks
- [ ] `Docs/architecture.png` (draw.io, Excalidraw or Mermaid)
- [ ] README written
- [ ] Commit

---

## Session 3: Eval report + design decisions
- [ ] `Docs/eval-report.md`: method, cases, results per model, **failures with analysis**, and the retrieval metrics
- [ ] `Docs/design-decisions.md`: covers the questions below. **This is your interview prep doc**
  - Why a hand-written loop instead of a framework
  - Why the proposal + confirm pattern
  - Why 404 instead of 403
  - Why the idempotency key lives in the DB
  - Why a local model, and what the trade-offs were
  - RAG vs putting everything in the prompt at this scale
  - What you'd change for real production use
- [ ] Commit

---

## Session 4: Demo video (3–5 min)
Script (from the brief, §10.1):
1. The problem, and what is simulated (30s)
2. The architecture diagram (30s)
3. A policy question answered with a citation
4. An order lookup, then a blocked cross-customer request
5. The return flow, with the confirmation dialog and the duplicate retry
6. The order service down, giving an honest error
7. Eval results, traces and the model comparison
8. Lessons learned and limitations

- [ ] Record it (QuickTime/OBS), with captions
- [ ] Upload it (YouTube unlisted or LinkedIn native) and link it in the README

---

## Session 5: Publish
- [ ] LinkedIn: the full demo walkthrough video post
- [ ] LinkedIn: "What a real shop owner taught me about my assumptions" (from `Docs/seller-feedback.md`)
- [ ] CV project entry (adapt the brief's §11.1 to your actual numbers)
- [ ] Pin the repo on GitHub and add topics (fastapi, flutter, llm, rag, tool-calling, evals)
- [ ] LinkedIn Featured section: the repo and the video

---

## ✅ Project done when
- [ ] A fresh clone runs with 3 commands
- [ ] README, diagram, eval report and design decisions are published
- [ ] The video is published
- [ ] All weekly posts are out
- [ ] CV is updated

## After the project (from the brief, §13)
1. Show it to someone who does customer-support work
2. Revise the wrong assumptions
3. Optional: a Shopify dev-store adapter behind the same tool interface
4. Any real pilot only with explicit permission, starting with test or read-only data
