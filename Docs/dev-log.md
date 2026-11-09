# Dev Log
- Did:
- Learned:
- Stuck on / surprised by:

### Interview Q&A
1. down vs down -v:-v is how I reset to a clean database; without it Postgres data can survives restarts.

2. Why Ollama runs on the Mac and not in Docker
-- This is a macOS limitation. On a Linux server with an NVIDIA GPU, Ollama runs fine in Docker with the NVIDIA container toolkit.
-- So in production you could containerize it. Locally, the Mac's Metal GPU wins.

3. What to do if a secret leaks
--Rewriting history doesn't make the secret safe again. If the repo was ever public, assume it's already been copied by forks, clones, and bots that scan GitHub within minutes. Rotating the key is the real fix; cleaning history is only tidying up.

4. Dependency injection vs a global DB connection
--What's bad is a single global connection or session. Concurrent requests would interleave transactions on it, one request's failed transaction would poison the others, and there's no pool to recover from a dropped connection.
--DI doesn't create a "fresh connection" per request. A yield dependency hands each request its own session, which borrows a connection from the pool and returns it at the end. "Fresh connection" vs "pooled session" is exactly the detail interviewers check

5. Why localhost inside a container isn't your Mac
--To be precise, host.docker.internal is a hostname that resolves to your Mac's IP.
--Docker Desktop provides it automatically. On Linux it doesn't exist unless you add extra_hosts: host-gateway, which is why your compose file includes that line. It keeps the setup portable.

## 2026-11-06
- Did:Init. proj. structure, configured env for repository hygiene, and initialized a Postgres database via Docker Compose.
- Learned:Learned that `git mv` tracks file renames cleanly in source control, Initialization database via Docker Compose, importance of logging, logger
- Stuck on / surprised by: docker-compose.yml ..make taks command more easier

## 2026-11-09
- Did: API container creation, ollama model connection t container
- Learned:Dockerfile writing, .dockerignore writing importance
- Stuck on / surprised by:
