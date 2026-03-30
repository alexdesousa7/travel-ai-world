# 🚀 FastAPI Professional Boilerplate Template

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

A production-ready, highly opinionated **FastAPI Template** designed to build scalable async web APIs. It provides a solid foundation with "batteries included" for user authentication, layered architecture, database migrations, and **built-in Artificial Intelligence integration**.

## ✨ Features (Batteries Included)

- 🏗️ **Layered Architecture:** Controllers (Routers), Services, Repositories, and Models logically separated.
- 🔐 **Authentication & RBAC:** JWT Bearer tokens, Bcrypt hashing, and built-in **Role-Based Access Control** (Admin/User).
- 👥 **User Module:** A complete, working User entity (CRUD operations, login, role management).
- 💾 **Database Connectivity:** Async PostgreSQL connections via `asyncpg` and `SQLAlchemy 2.0`.
- 🗃️ **Migrations:** Alembic is pre-configured and ready to auto-generate schemas.
- 🚦 **Error Handling:** Centralized semantic exception handling extending `HTTPException`.
- 🧪 **Testing Base:** `pytest-asyncio` configured with an in-memory test database and coverage reporting.
- 🚀 **Blazing Fast CI/CD & Deps:** GitHub Actions workflow utilizing `uv` caching (with `.lock` deterministic builds), `Ruff` formatting, and `Mypy` type checking.

---

## 🛠️ Quick Start Guide

### 1. Prerequisites ⚡

The only tool you need to manage this project is **[uv](https://github.com/astral-sh/uv)**. It replaces `pip`, `venv`, and `pip-tools` with a single, ultra-fast interface.

**Install `uv` globally:**
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Via pip:**
  ```bash
  pip install uv
  ```

**Why `uv`?**
- **Speed**: Resolves and installs dependencies significantly faster than `pip`.
- **Determinism**: The `uv.lock` file ensures you install the exact same versions across all environments.
- **Convenience**: `uv run` executes commands in the managed virtual environment without requiring manual activation.

### 2. Installation & Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd travel-ai-world

# 2. Enter the backend directory
cd backend

# 3. Setup environment and install dependencies
# Note: We use --all-extras to install testing tools (pytest) and linters (ruff).
# By default, `uv sync` only installs the core dependencies needed to run the API 
# in production. This intentional separation keeps the production image lightweight 
# and secure, while using `--all-extras` gives developers locally all the tools they need.
uv sync --all-extras
```

### 3. Environment Configuration

Copy the `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

> [!IMPORTANT]
> The `.env.example` file defaults to PostgreSQL and Docker (`DB_SERVER="db_postgres"`).
> **If you are running the backend locally without Docker**, you MUST open `.env` and change `DB_SERVER="127.0.0.1"`. You also need a PostgreSQL server running locally, or you can switch `DB_ENGINE="sqlite"` to use a simple file-based database for quick testing.
>
> **CORS (production):** Set `BACKEND_CORS_ORIGINS` to your frontend URL(s) — e.g. `BACKEND_CORS_ORIGINS=["https://yourdomain.com"]`. The default value allows only `localhost:3000` and `localhost:5173`.

### 4. Database Setup

Once your `.env` is properly configured and pointing to a running database (or sqlite), apply migrations to create the underlying tables:

```bash
uv run alembic upgrade head
```

### 5. Run the API

Start the local development server:

```bash
uv run fastapi dev app/main.py
```

Then visit:

- **Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Interactive Spec:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ✅ Running Tests

The test suite runs against a **dedicated PostgreSQL database** named `<DB_NAME>_test` (auto-created from your `.env` `DB_NAME` value). Schema is rebuilt fresh on every run, so your development data is never touched.

```bash
uv run pytest -v
```

## 🏗️ Project Architecture Layout

If you intend to add a new `Item` feature, you should follow this exact sequence:

1. `app/models/item.py` — Create the SQLAlchemy model inheriting from `Base`.
2. `app/models/__init__.py` — Import `Item` here so Alembic and the test harness discover it.
3. `app/schemas/item.py` — Define Pydantic inputs and outputs (`ItemCreate`, `ItemResponse`).
4. `app/repositories/item_repository.py` — Handle solely DB operations (`create`, `get_by_id`).
5. `app/services/item_service.py` — Hold business rules.
6. `app/api/v1/endpoints/items.py` — Handle HTTP traffic and inject dependencies via `Depends()`.
