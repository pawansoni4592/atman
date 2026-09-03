# Architecture

Architecture notes and diagrams for Atman.

## Initial system

```text
Next.js Web / Admin
        |
        v
    FastAPI API
        |
  +-----+-----+
  |     |     |
 AI   Memory  Planner
  |     |     |
  +-----+-----+
        |
 PostgreSQL + pgvector
```

The first implementation will keep the architecture modular while avoiding premature microservices.
