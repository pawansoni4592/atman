# Atman

> A personal AI mentor that remembers, learns, plans, and helps you make better decisions over time.

## Vision

Atman is designed as a long-term personal assistant with persistent memory, goals, tasks, planning, and specialized AI capabilities.

## Initial Architecture

- `apps/web` — Next.js user application
- `apps/api` — FastAPI backend
- `apps/admin` — Admin dashboard
- `packages/ai` — AI and agent logic
- `packages/database` — Database models and migrations
- `packages/shared` — Shared contracts and utilities
- `packages/ui` — Shared UI components
- `docs` — Architecture, product, and technical decisions
- `infrastructure` — Local/deployment infrastructure
- `scripts` — Developer automation

## Development Philosophy

Keep `main` stable. Build features in short-lived `feature/*` branches and merge completed, tested work into `main`.

## Status

🚧 Early development — repository foundation.
