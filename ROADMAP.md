# Perplexity-like Platform — Feature Roadmap

A phased build plan for an AI answer/chat platform. Features are ordered so each
phase ships something usable on its own and lays groundwork for the next.
Cross-cutting concerns (auth, RBAC, billing, usage) are intentionally **last** so
we don't over-engineer before the core product works.

Architecture: FastAPI + hexagonal/DDD, one module per bounded context under
`app/modules/<module>/` (domain / application / infrastructure / presentation).

Legend: `[ ]` planned · `[~]` in progress · `[x]` done

---

## Phase 0 — Foundation (mostly done)

The plumbing every other phase depends on.

- [x] FastAPI app skeleton + router wiring
- [x] Hexagonal module layout (domain / application / infra / presentation)
- [x] Config via settings (`app/shared/config`)
- [x] Database setup + sessions (`app/shared/database`)
- [x] Global exception handlers
- [ ] Structured logging + request IDs
- [ ] Health/readiness endpoints (`/health`, `/ready`)
- [ ] Dockerfile + docker-compose (app + Postgres)
- [ ] Test harness (pytest) + CI
- [ ] Alembic migrations

---

## Phase 1 — Core Chatbot (`module: chat`)

A working conversational chatbot with a real LLM. **This is the MVP.**

- [x] Conversation + Message domain models (aggregate root + entity in `kernel`)
- [x] Conversation repository (SQLAlchemy)
- [x] LLM port + echo adapter (echo is the default, no-key provider)
- [x] Real LLM adapter — **multi-provider** (Anthropic / OpenAI / Ollama / HuggingFace) via LangChain + LangGraph
- [x] Streaming responses (SSE) — `POST /chats/{id}/messages/stream`
- [x] System prompts / persona configuration (`LLM_SYSTEM_PROMPT`)
- [x] Multi-turn memory within a conversation (full history passed each turn)
- [x] List conversations (`GET /chats`) + create/get + delete (repo)
- [ ] Context-window management (truncation/trimming) — naive full-history today
- [ ] Stop / regenerate / edit-and-resend a message
- [ ] Rename / delete conversation endpoints (delete exists in repo, no route yet)
- [ ] Token counting + per-message metadata
- [ ] Basic frontend chat UI (API contract is live; UI pending)

**Done when:** a user can hold a multi-turn streaming conversation that persists. ✅ (API)

---

## Phase 2 — File Support / RAG (`module: documents`, `module: rag`)

Upload documents, index them, and let the chatbot answer grounded in them.

### 2a. Ingestion
- [ ] File upload endpoint (PDF first, then docx/txt/md/csv)
- [ ] File storage abstraction (local disk → S3-compatible later)
- [ ] Document + chunk domain models
- [ ] Text extraction (PDF parsing) + cleanup
- [ ] Chunking strategy (size/overlap, semantic chunking later)

### 2b. Indexing
- [ ] Embeddings port + adapter
- [ ] Vector store integration (pgvector to start — already on Postgres)
- [ ] Embedding + storing chunks with metadata (source, page, doc id)
- [ ] Re-index / delete-by-document

### 2c. Retrieval & generation
- [ ] Semantic search over chunks (top-k)
- [ ] Hybrid search (keyword + vector) + reranking
- [ ] RAG prompt assembly (inject retrieved context)
- [ ] **Inline citations** mapping answer spans → source chunks
- [ ] "Chat with your documents" scoped to a collection
- [ ] Document collections / folders

**Done when:** a user uploads a PDF and gets cited, grounded answers.

---

## Phase 3 — Web Search & Browsing (`module: search`)

The "Perplexity" core: answer from the live web with sources.

- [ ] Web search provider port + adapter (Brave/SerpAPI/Tavily/etc.)
- [ ] Fetch + extract page content (readability/boilerplate removal)
- [ ] Rank + select sources for the query
- [ ] Synthesize answer over fetched sources with **inline citations**
- [ ] Source cards (title, favicon, snippet, URL)
- [ ] Follow-up questions / "related" suggestions
- [ ] Query routing: decide chat-only vs RAG vs web (or combine)
- [ ] Freshness / recency handling
- [ ] Caching of search + fetch results

**Done when:** a user asks a current-events question and gets a sourced answer.

---

## Phase 4 — Answer Quality & UX

Make answers feel polished and trustworthy.

- [ ] Streaming with citation rendering as text arrives
- [ ] Markdown / code / table rendering
- [ ] Image & media in answers (where sources have them)
- [ ] "Focus" modes (Web / Academic / Writing / your Docs)
- [ ] Follow-up threading that keeps prior sources in context
- [ ] Answer feedback (thumbs up/down, report)
- [ ] Shareable answer / conversation links
- [ ] Export conversation (markdown / PDF)

---

## Phase 5 — Search Power Features

- [ ] Multi-step / agentic research (decompose → search → synthesize)
- [ ] File + web combined in one query
- [ ] Saved searches / collections / spaces
- [ ] Scheduled / recurring research
- [ ] Multiple model selection (let users pick the model)
- [ ] Image input (multimodal questions)
- [ ] Voice input / output (optional)

---

## Phase 6 — Auth & Identity (`module: identity`)

Now that the product works, gate it behind accounts.

- [ ] User registration + login (email/password)
- [ ] Password hashing (argon2/bcrypt) + reset flow
- [ ] JWT / session tokens + refresh
- [ ] OAuth / social login (Google, GitHub)
- [ ] Email verification
- [ ] API keys for programmatic access
- [ ] Account settings / profile
- [ ] Associate conversations & documents with a user

---

## Phase 7 — RBAC & Multi-tenancy (`module: identity` / `org`)

- [ ] Roles (owner / admin / member / viewer)
- [ ] Permission checks at the use-case layer (decorators/guards)
- [ ] Organizations / teams / workspaces
- [ ] Invitations + member management
- [ ] Shared vs private collections/spaces
- [ ] Per-resource access control (docs, conversations, spaces)
- [ ] Audit log of sensitive actions

---

## Phase 8 — Usage, Plans & Billing (`module: billing`, `module: usage`)

- [ ] Usage metering (tokens, queries, searches, storage) per user/org
- [ ] Rate limiting + quota enforcement (middleware/guard)
- [ ] Plan definitions (Free / Pro / Team / Enterprise)
- [ ] Feature gating by plan (model access, web search limits, seats)
- [ ] Stripe integration (checkout, subscriptions, webhooks)
- [ ] Invoices + payment history
- [ ] Usage dashboard for users
- [ ] Overage / pay-as-you-go handling
- [ ] Trials, coupons, upgrades/downgrades, cancellation

---

## Phase 9 — Operations & Hardening (ongoing)

- [ ] Observability: metrics, tracing, dashboards
- [ ] Cost tracking per request (LLM + search spend)
- [ ] Admin panel (users, orgs, usage, moderation)
- [ ] Content moderation / safety filters
- [ ] Abuse / fraud prevention
- [ ] Backups + disaster recovery
- [ ] Load testing + autoscaling
- [ ] Security review + pen test
- [ ] GDPR: data export & deletion

---

## Suggested module map

| Phase | Module(s)                          |
|-------|------------------------------------|
| 1     | `chat`                             |
| 2     | `documents`, `rag`                 |
| 3     | `search`                           |
| 4–5   | enhancements across above modules  |
| 6     | `identity`                         |
| 7     | `identity` / `org`                 |
| 8     | `billing`, `usage`                 |

## Guiding principles

- Ship each phase end-to-end before starting the next.
- Keep the LLM, embeddings, vector store, search, and storage behind **ports** so
  providers are swappable.
- Defer auth/billing until the core answer engine is genuinely good.
- Citations are a first-class concern from Phase 2 onward — never bolt them on.
