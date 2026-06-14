# Architecture

**Style:** Modular Monolith
**Patterns:** Clean Architecture · Hexagonal (Ports & Adapters) · CQRS · DDD (medium)
**Stack:** FastAPI · SQLAlchemy · Pydantic · LangChain + LangGraph

This is the Python/FastAPI translation of the reference TypeScript layout. Same
ideas, Python conventions: packages are `snake_case`, classes are `PascalCase`,
every directory is a package (`__init__.py`). Root package is `app/` (not `src/`).

---

## Top-level layout

```
app/
├── main.py                 # APP ENTRY — builds the FastAPI app via bootstrap
│
├── bootstrap/              # composition root — wires the whole monolith
│   ├── application_bootstrap.py   # create_app(): FastAPI factory
│   ├── dependency_container.py    # central DI container (singletons/factories)
│   ├── route_registry.py          # register every module's router
│   └── environment.py             # env loading (wraps shared config)
│
├── modules/               # one bounded context per folder (see module shape)
│   ├── chat/              # ← Phase 1 (this build)
│   ├── files/             # Phase 2 — uploads / RAG ingestion
│   ├── search/            # Phase 3 — web search
│   ├── auth/              # Phase 6
│   ├── users/             # Phase 6
│   └── billing/           # Phase 8
│
├── shared/                # cross-cutting, no business logic
│   ├── kernel/            # DDD building blocks (Entity, AggregateRoot, …)
│   ├── middleware/
│   ├── exceptions/
│   ├── constants/
│   ├── decorators/
│   ├── types/
│   └── utils/
│
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## Module shape (every module is identical)

Each module is a self-contained hexagon with four layers. Dependencies point
**inward**: `adapters → application → domain`. `infrastructure` holds the
technical wiring an adapter needs. The domain depends on nothing.

```
modules/<module>/
│
├── domain/                          # PURE business core — no framework, no IO
│   ├── entities/                    # entities + aggregate roots
│   ├── value_objects/               # immutable VOs (ids, email, role, …)
│   ├── services/                    # domain services (logic spanning entities)
│   ├── rules/                       # policies / invariants
│   ├── events/                      # domain events
│   └── exceptions/                  # domain-specific errors
│
├── application/                     # USE CASES — orchestrates the domain (CQRS)
│   ├── commands/                    # writes: one folder per command
│   │   └── <command>/
│   │       ├── <command>_command.py # the Command (a frozen dataclass = intent)
│   │       └── <command>_handler.py # the Handler (implements an input port)
│   ├── queries/                     # reads: one folder per query
│   │   └── <query>/
│   │       ├── <query>_query.py
│   │       └── <query>_handler.py
│   ├── ports/
│   │   ├── input/                   # driving ports — use-case interfaces (ABCs)
│   │   └── output/                  # driven ports — repo/llm/cache/… interfaces
│   ├── dto/                         # request/response/result data shapes
│   └── mappers/                     # domain ⇆ dto translation
│
├── adapters/                        # the edges — everything that touches IO
│   ├── input/                       # driving adapters (call INTO the app)
│   │   ├── http/                    # controller + routes + middleware
│   │   ├── events/                  # event/message consumers
│   │   └── scheduler/               # cron / background jobs
│   └── output/                      # driven adapters (app calls OUT)
│       ├── persistence/             # ORM models, repository impls, mappers
│       ├── cache/
│       ├── notification/
│       ├── llm/                     # LangChain/LangGraph model adapter (chat)
│       └── events/                  # event publishers
│
└── infrastructure/                  # technical config for this module's adapters
    ├── database/                    # connection / session / tx manager
    ├── cache/
    ├── messaging/
    ├── config/                      # module config object
    └── observability/               # logger / metrics
```

### TS → Python naming map

| Reference (TS)            | Here (Python)                                      |
|---------------------------|----------------------------------------------------|
| `User.ts`                 | `entities/user.py` → `class User`                  |
| `value-objects/Email.ts`  | `value_objects/email.py` → `class Email`           |
| `RegisterCommand.ts`      | `commands/register/register_command.py`            |
| `RegisterHandler.ts`      | `commands/register/register_handler.py`            |
| `RegisterUseCase.ts` (interface) | `ports/input/register_use_case.py` (ABC)    |
| `UserRepositoryPort.ts`   | `ports/output/user_repository_port.py` (ABC)       |
| `AuthController.ts`       | `adapters/input/http/controller.py`                |
| `AuthRoutes.ts`           | `adapters/input/http/routes.py`                    |
| `PostgresUserRepository.ts` | `adapters/output/persistence/<...>_repository.py`|
| `JwtTokenAdapter.ts`      | `adapters/output/token/jwt_token_adapter.py`       |
| `kernel/AggregateRoot.ts` | `shared/kernel/aggregate_root.py`                  |

### CQRS in this codebase (medium DDD)

- A **Command** is an immutable intent (`@dataclass(frozen=True)`). A **Query**
  is the same for reads.
- A **Handler** executes exactly one command/query. It implements an **input
  port** (an ABC in `ports/input/`) so the HTTP controller depends on the
  interface, not the concrete handler.
register_result.py- Handlers depend only on **output ports** (`ports/output/`). Concrete adapters
  (SQLAlchemy repo, LangChain LLM) are bound in the DI container — the core
  never imports a framework.
- No mediator/bus yet (that's "heavy" DDD). Controllers resolve handlers via
  FastAPI `Depends`. A bus can be slotted in later without touching handlers.

### The dependency rule

```
adapters/input  →  application  →  domain  ←  application  ←  adapters/output
                         ↑                                          │
                         └──────── depends only on ports ───────────┘
infrastructure  →  supports adapters (never imported by domain/application)
```

---

## Where Phase 1 (chat) lives

```
modules/chat/
├── domain/
│   ├── entities/        conversation.py (aggregate root), message.py
│   ├── value_objects/   message_role.py
│   ├── events/          message_posted.py
│   └── exceptions/      chat_exceptions.py
├── application/
│   ├── commands/
│   │   ├── create_conversation/   *_command.py, *_handler.py
│   │   └── send_message/          *_command.py, *_handler.py
│   ├── queries/
│   │   ├── get_conversation/      *_query.py, *_handler.py
│   │   └── list_conversations/    *_query.py, *_handler.py
│   ├── ports/
│   │   ├── input/    create_conversation_use_case.py, send_message_use_case.py,
│   │   │             get_conversation_use_case.py, list_conversations_use_case.py
│   │   └── output/   conversation_repository_port.py, llm_port.py
│   ├── dto/          send_message_result.py
│   └── mappers/      (domain ⇆ http handled in adapters/input/http/view_mapper.py)
├── adapters/
│   ├── input/http/   controller.py, routes.py, schemas.py, dependencies.py
│   └── output/
│       ├── persistence/  models/, conversation_mapper.py,
│       │                 sqlalchemy_conversation_repository.py
│       └── llm/          langchain_llm_adapter.py, model_factory.py,
│                         chat_graph.py, echo_llm_adapter.py
└── infrastructure/
    └── config/       chat_config.py   # provider/model/streaming settings
```

### LLM provider strategy

`llm_port.py` is the single seam. Behind it, a **LangChain + LangGraph** adapter
supports multiple providers, chosen at runtime via `LLM_PROVIDER`:

| `LLM_PROVIDER` | Backend                                   |
|----------------|-------------------------------------------|
| `anthropic`    | `langchain` `init_chat_model` (Claude)    |
| `openai`       | `langchain` `init_chat_model` (GPT)       |
| `ollama`       | local models via Ollama                   |
| `huggingface`  | `langchain-huggingface`                   |
| `echo`         | dependency-free stub (default, no keys)   |

`model_factory.py` builds the right LangChain chat model; `chat_graph.py` wraps
it in a minimal LangGraph `StateGraph` (one model node today, room for retrieval
/ tools in Phase 2+). Swapping providers never touches the domain or handlers.

---

## Phase order

See [ROADMAP.md](ROADMAP.md). Each phase adds one module (or enriches an
existing one) using the module shape above. Auth / RBAC / billing come last.
