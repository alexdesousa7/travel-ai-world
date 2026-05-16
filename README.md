# Travel AI World ✈️

> AI-powered travel planning. Tell us where you want to go — our AI crafts a personalized, day-by-day itinerary in seconds.

## Project Overview

Travel AI World is a full-stack web application where users input their destination, dates, budget, group size, and travel style, and an AI generates a complete itinerary for them via real-time streaming.

The project is split into independent services:

| Service | Stack | Status |
|---|---|---|
| **`frontend/`** | Next.js 16 · Tailwind CSS v4 · TypeScript | ✅ Active |
| **`backend/`** | FastAPI · Python 3.12 · NVIDIA AI (Kimi K2.6) | ✅ Active |
| **`Scraper/`** | Python · Playwright · httpx | 🔧 In development |

---

## Repository Structure

```
travel-ai-world/
├── frontend/          # Next.js web app (browser client)
├── backend/           # FastAPI REST API + AI chat streaming
├── Scraper/           # City data scrapers (Madrid, Berlin)
│   ├── Madrid/
│   └── Madrid2.0/
├── .github/workflows/ # CI/CD (PR checks + GitHub Pages deploy)
├── tasks.ps1          # Project task runner (setup, dev, lint, build, release)
├── scripts/           # Automation scripts (versioning, releases)
├── ideas.pen          # Pencil design file — landing page mockup & design system
├── images/            # Design assets and generated images
└── README.md          # ← You are here
```

---

## Quick Start

### Prerequisites

- **Node.js ≥ 20** — Frontend
- **Python ≥ 3.12 + [uv](https://github.com/astral-sh/uv)** — Backend
- A **Google Cloud OAuth Client ID** — for authentication

### Using the Task Runner (Recommended)

The `tasks.ps1` script provides a unified interface for all dev operations:

```powershell
.\tasks.ps1 setup          # Install all dependencies (frontend + backend)
.\tasks.ps1 dev-api        # Start FastAPI dev server (port 8000)
.\tasks.ps1 dev-frontend   # Start Next.js dev server (port 3000)
.\tasks.ps1 lint           # Lint both frontend and backend
.\tasks.ps1 test           # Run all tests
.\tasks.ps1 build          # Production build
.\tasks.ps1 docker-up      # Start backend + DB via Docker Compose
.\tasks.ps1 docker-down    # Stop Docker Compose services
.\tasks.ps1 check-port     # Check/kill process on port 8000
```

### Manual Setup

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). See [`frontend/README.md`](./frontend/README.md) for full details.

#### Backend

```bash
cd backend
uv sync --all-extras
cp .env.example .env      # Configure your environment variables
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

API docs at [http://localhost:8000/docs](http://localhost:8000/docs). See [`backend/README.md`](./backend/README.md) for full details.

### Environment Variables

#### Backend (`backend/.env`)

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | JWT signing secret |
| `GOOGLE_CLIENT_ID` | ✅ | Google OAuth Client ID (from Cloud Console) |
| `GOOGLE_CLIENT_SECRET` | ✅ | Google OAuth Client Secret |
| `NVIDIA_API_KEY` | ✅ | NVIDIA API key for AI chat |
| `DB_ENGINE` | | `postgresql`, `mysql`, or `sqlite` (default: `postgresql`) |
| `FRONTEND_URL` | | Frontend origin for CORS (default: `http://localhost:3000`) |

#### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend URL (default: `http://localhost:8000`) |
| `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | ✅ | Same Google Client ID as backend |

---

## Authentication

Travel AI World uses **Google OAuth 2.0 exclusively** — there is no password-based login.

**Flow:**
1. User clicks "Sign in with Google" → Google returns an ID token
2. Frontend sends the token to `POST /api/v1/auth/google`
3. Backend verifies the token with Google, creates/updates the user in DB
4. Backend returns a JWT for subsequent authenticated API calls

---

## AI Chat

The trip planner (`PlannerCard`) streams AI-generated itineraries in real-time:

- **Backend**: `POST /api/v1/chat` — SSE streaming proxy to NVIDIA Kimi K2.6
- **Frontend**: `streamChat()` in `services/api.ts` consumes SSE chunks
- **Fallback**: When `NEXT_PUBLIC_API_URL` is not set, the UI shows a static "coming soon" mode (for GitHub Pages deployments)

---

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/google` | — | Google OAuth login → JWT |
| `POST` | `/api/v1/chat` | — | AI chat streaming (SSE) |
| `GET` | `/api/v1/users/me` | Bearer | Current user profile |
| `GET` | `/api/v1/health/` | — | API health check |
| `CRUD` | `/api/v1/trips/` | Bearer | Trip management |
| `CRUD` | `/api/v1/destinations/` | Bearer | Destination management |
| `CRUD` | `/api/v1/itinerary-days/` | Bearer | Itinerary day management |
| `CRUD` | `/api/v1/activities/` | Bearer | Activity management |
| `CRUD` | `/api/v1/meals/` | Bearer | Meal management |
| `CRUD` | `/api/v1/accommodations/` | Bearer | Accommodation management |
| `CRUD` | `/api/v1/transportations/` | Bearer | Transportation management |

---

## CI/CD

### PR Checks (`.github/workflows/pr.yml`)

Every pull request triggers:
1. **Backend**: `ruff check` + `ruff format --check` + import validation
2. **Frontend**: `npm ci` + `npm run build`

### GitHub Pages Deploy (`.github/workflows/deploy.yml`)

Every push to `main`:
1. **Build** — `npm run build` with `NEXT_PUBLIC_BASE_PATH=/travel-ai-world`
2. **SPA fallback** — copies `out/index.html` → `out/404.html`
3. **Deploy** — uploads `out/` to GitHub Pages

Live at: 👉 `https://manupm87.github.io/travel-ai-world/`

---

## Docker Deployment

The backend includes a production-ready Docker setup:

```powershell
.\tasks.ps1 docker-up       # Build + start API + PostgreSQL
.\tasks.ps1 docker-down     # Stop all services
.\tasks.ps1 docker-logs     # Tail API logs
.\tasks.ps1 docker-rebuild  # Rebuild API image (no cache)
```

**Architecture:**
- **Multi-stage Dockerfile** — builder stage (uv + gcc) → slim production image (no build tools)
- **Non-root user** (`appuser`) for security
- **Auto-migrations** — `entrypoint.sh` runs `alembic upgrade head` on startup
- **Healthcheck** on PostgreSQL before API starts

**Manual Docker Compose:**

```bash
cd backend
cp .env.example .env       # Configure env vars
docker compose up --build
```

> **Note:** When running inside Docker Compose, `DB_SERVER` is automatically overridden to `db_postgres` (the Compose service name).

---

## Branding & Assets

- **Logo:** White airplane silhouette on a rounded indigo square (#4F6EF7)
- **Custom Favicon:** Dedicated `icon.png` for browser tabs
- **Iconography:** Professional SVG icons from [Lucide](https://lucide.dev/)

---

## Roadmap

- [x] Landing page (`/`)
- [x] EN 🇬🇧 / ES 🇪🇸 i18n
- [x] AI trip planner form (`/plan`)
- [x] Trip itinerary viewer (`/trip/[id]`)
- [x] FastAPI backend with layered architecture
- [x] Google OAuth 2.0 authentication
- [x] AI chat streaming (NVIDIA Kimi K2.6)
- [x] CI/CD pipeline (PR checks + GitHub Pages)
- [x] Dev tooling (`tasks.ps1` task runner)
- [ ] User saved trips & dashboard
- [ ] PDF Export for itineraries
- [ ] Dark mode toggle customization
