# DocSentinel — Technology Stack & Decision Rationale

Every technology below was chosen against four priorities: **open source, production-readiness, community support, and low barrier to team-wide adoption** (all three engineers are learning as they build).

## Frontend

**Chosen: React + Vite + TypeScript + Tailwind CSS**

| | React (Vite) | Next.js | Vue |
|---|---|---|---|
| Purpose fit | SPA, talks to a separate FastAPI backend | Full-stack framework (SSR, API routes) | SPA, talks to separate backend |
| Learning curve | Moderate | Higher (SSR concepts, routing conventions) | Lower |
| Industry adoption | Very high | Very high | High, smaller in enterprise |
| Advantages | Huge ecosystem, flexible, fast Vite dev server | Built-in SSR/routing, great for SEO-heavy sites | Simple syntax, gentle learning curve |
| Disadvantages | More setup decisions (routing, state) | Overkill for a pure SPA talking to its own API | Smaller US enterprise footprint |
| Verdict | **Chosen** — DocSentinel doesn't need SSR; a decoupled SPA keeps frontend/backend independently deployable | Not needed | Smaller community for advanced AI-UI patterns |

TypeScript is used over plain JavaScript for compile-time type safety on API response shapes (e.g. the ingestion contract). Tailwind CSS is used over hand-written CSS/Bootstrap for fast, consistent styling without fighting specificity conflicts.

## Backend

**Chosen: FastAPI (Python)**

| | FastAPI | Django REST | Express (Node) |
|---|---|---|---|
| Async support | Native | Limited (ASGI support improving) | Native |
| AI/ML ecosystem fit | Excellent (same language as OCR/embeddings/LLM code) | Excellent | Weak |
| Auto API docs | Built-in (OpenAPI/Swagger) | Requires extra packages | Requires extra packages |
| Learning curve | Moderate | Higher (batteries-included conventions) | Lower |
| Industry adoption | High, fast-growing | Very high (mature) | Very high |
| Verdict | **Chosen** — Python-native means OCR, embedding, and LLM calls live in the same codebase as the API, with no cross-language glue | Heavier than needed for an API-only backend | Would require a second language for AI code |

## Database (Relational)

**Chosen: PostgreSQL**

| | PostgreSQL | MongoDB | MySQL |
|---|---|---|---|
| Data model fit | Structured (users, roles, documents, metadata) with JSONB flexibility where needed | Schema-less, better for unstructured docs | Structured, similar to Postgres |
| ACID guarantees | Full | Weaker multi-document transactions historically | Full |
| Industry adoption | Very high | High for document-style workloads | Very high |
| Verdict | **Chosen** — DMS core data (permissions, document ownership, audit logs) is inherently relational; JSONB columns cover flexible metadata without needing a second database | Would fragment data model across two paradigms | No meaningful advantage over Postgres here |

## Vector Database

**Chosen: ChromaDB**

| | ChromaDB | Pinecone | Weaviate |
|---|---|---|---|
| Hosting | Self-hosted / embedded | Managed cloud only | Self-hosted or managed |
| Cost | Free | Paid (usage-based) | Free (self-hosted) |
| Setup complexity | Very low | Low (but vendor account required) | Moderate |
| Industry adoption | Growing fast, popular in RAG projects | High in production SaaS | High, enterprise-grade |
| Verdict | **Chosen for build phase** — zero cost, zero external dependency, ideal for a student project and demoable offline | Best if scaling to production SaaS later | Strong alternative to mention as a production upgrade path |

## Authentication

**Chosen: JWT (JSON Web Tokens)**

| | JWT | Session-based (server-side sessions) | OAuth2 (third-party) |
|---|---|---|---|
| Statelessness | Fully stateless | Requires session store (Redis) | Depends on provider |
| Fit for REST API | Excellent | Requires sticky sessions or shared store | Adds external dependency |
| Verdict | **Chosen** — stateless tokens scale horizontally without a shared session store; role claims embedded in the token drive RBAC | Adds infra (Redis) not otherwise needed | Unnecessary for an internal-organization DMS |

## OCR

**Chosen: Tesseract OCR**

| | Tesseract | EasyOCR | Cloud OCR (Google Vision / AWS Textract) |
|---|---|---|---|
| Cost | Free | Free | Pay-per-use |
| Accuracy | Good for clean scans | Good, better on some fonts/languages | Best overall |
| Deployment | Fully self-hosted, no internet needed | Fully self-hosted | Requires internet + API key |
| Verdict | **Chosen** — free, self-hosted, keeps the whole pipeline demoable without cloud credentials; document cloud OCR as a production upgrade path | Viable alternative if Tesseract accuracy is insufficient for a specific dataset | Best for production accuracy, adds cost/dependency |

## Embeddings

**Chosen: BAAI/bge-small-en-v1.5 (local, via sentence-transformers)**

| | bge-small-en-v1.5 | OpenAI text-embedding-3 | Cohere embeddings |
|---|---|---|---|
| Cost | Free, runs locally | Paid API | Paid API |
| Latency | Local (no network round-trip) | Network-dependent | Network-dependent |
| Quality | Strong for its size, competitive on retrieval benchmarks | Higher, especially on nuanced semantic tasks | Strong, similar tier to OpenAI |
| Verdict | **Chosen** — no API cost/key required for a student project; swappable later behind an embedding-service interface | Consider for production if budget allows | Alternative if already using Cohere elsewhere |

## LLM

**Chosen: Ollama (development) with optional OpenAI (production)**

| | Ollama (local models) | OpenAI API | Anthropic API |
|---|---|---|---|
| Cost | Free (local compute) | Pay-per-token | Pay-per-token |
| Setup | Local install, no key needed | API key required | API key required |
| Quality ceiling | Good for demos, capped by local model size/hardware | Very high | Very high |
| Verdict | **Chosen for dev** — free iteration during development; the RAG orchestration code calls an LLM interface, so swapping to OpenAI/Anthropic in production is a config change, not a rewrite |

## Storage

**Chosen: Local disk (Week 1) → MinIO (Week 2+) → AWS S3 (optional prod)**

| | Local disk | MinIO | AWS S3 |
|---|---|---|---|
| Cost | Free | Free (self-hosted) | Pay-per-use |
| Prod-realistic | No | Yes (same S3 API) | Yes |
| Verdict | Dev only | **Chosen for build phase** — S3-compatible API means the storage service code is identical whether pointed at MinIO or real S3 | Drop-in replacement if deploying to AWS |

## Deployment

**Chosen: Docker + Docker Compose**

| | Docker Compose | Kubernetes | Bare-metal/manual |
|---|---|---|---|
| Setup complexity | Low | High | Low but not reproducible |
| Fit for a 3-person student project | Excellent | Overkill | Poor (environment drift between machines) |
| Verdict | **Chosen** — one command (`docker compose up`) reproduces the entire stack (Postgres, Chroma, MinIO, backend, frontend) identically on any teammate's or judge's machine; Kubernetes is mentioned in the report as a natural production-scaling path |

## Technology Decision Matrix

| Layer | Technology | Primary reason |
|---|---|---|
| Frontend | React + Vite + TS + Tailwind | Decoupled SPA, type safety, fast styling |
| Backend | FastAPI | Python-native AI integration, async, auto docs |
| Relational DB | PostgreSQL | ACID, JSONB flexibility, industry standard |
| Vector DB | ChromaDB | Free, zero-ops, ideal for build phase |
| Auth | JWT | Stateless, scales horizontally |
| OCR | Tesseract | Free, self-hosted, no external dependency |
| Embeddings | BAAI/bge-small-en-v1.5 | Free, local, competitive quality |
| LLM | Ollama (dev) / OpenAI (prod) | Free iteration, swappable for production quality |
| Storage | Local → MinIO → S3 | Progressive, same API throughout |
| Deployment | Docker Compose | Reproducible, low-ops, team-friendly |
