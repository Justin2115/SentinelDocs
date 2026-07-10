# DocSentinel — Folder Structure

```
DocSentinel/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint, router registration
│   │   ├── api/                 # Route handlers grouped by domain (auth, documents, query)
│   │   ├── services/             # Business logic: upload, ocr, chunking, embedding, rag
│   │   ├── models/               # SQLAlchemy ORM models (User, Role, Document, Metadata)
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   ├── core/                  # Config, security (JWT), dependency injection
│   │   └── db/                    # DB session setup, migrations entrypoint
│   ├── tests/                     # Pytest unit/integration tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Route-level views (Upload, Search, Chat, Admin)
│   │   ├── api/                    # Typed API client functions
│   │   ├── hooks/                  # Custom React hooks
│   │   └── types/                  # Shared TypeScript types (mirrors backend schemas)
│   ├── package.json
│   └── Dockerfile
│
├── ocr/                             # OCR-specific scripts, isolated so it can become
│                                     # its own worker/service later without touching backend/
│
├── ingestion/                        # Format parsers (PDF, DOCX, XLSX, email, image)
│                                      # Each parser outputs the shared ingestion contract shape
│
├── storage/                          # Local dev file storage (gitignored contents)
│
├── vector_db/                        # ChromaDB persistence directory (gitignored)
│
├── database/
│   ├── migrations/                   # Alembic migration scripts
│   └── schema.sql                     # Reference schema dump
│
├── docker/
│   ├── docker-compose.yml             # Orchestrates backend, frontend, postgres, chroma, minio
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── scripts/                            # One-off setup/maintenance scripts (seed data, backfills)
│
├── docs/                                # This documentation set
│   ├── ARCHITECTURE.md
│   ├── TECH_STACK.md
│   ├── FOLDER_STRUCTURE.md
│   ├── PROJECT_ARCHITECTURE_OVERVIEW.md
│   └── ingestion-contract.md
│
├── .env.example                          # Documents required env vars without real secrets
├── .gitignore
└── README.md
```

## Purpose of key files

- **`backend/app/services/`** — this is where the actual business logic lives (upload validation, OCR invocation, chunking, embedding, RAG orchestration). Keeping this separate from `api/` (routing) follows a service-layer architecture: routes stay thin, logic stays testable in isolation.
- **`backend/app/core/security.py`** (inside `core/`) — JWT creation/validation and password hashing live here, isolated so authentication logic isn't duplicated across routes.
- **`ingestion/`** — one parser module per file type, each conforming to the shared ingestion contract (see `ingestion-contract.md`). This is what lets Person B and C's code stay format-agnostic.
- **`docker/docker-compose.yml`** — single source of truth for how all services (backend, frontend, Postgres, Chroma, MinIO) are wired together; this is what a teammate or judge runs to get the whole system up.
- **`.env.example`** — lists every environment variable the system needs (DB URL, JWT secret, Chroma path, MinIO credentials) without committing actual secrets — real `.env` is gitignored.
- **`storage/` and `vector_db/`** — both gitignored; they hold runtime data, not source code, and should never be committed.
