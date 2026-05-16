param(
    [string]$Task = "help"
)

switch ($Task) {
    "setup" {
        Write-Host "== Creating .env from template ==" -ForegroundColor Cyan
        if (-Not (Test-Path "backend\.env")) { Copy-Item "backend\.env.example" "backend\.env" }
        if (-Not (Test-Path "frontend\.env.local")) { Copy-Item "frontend\.env.example" "frontend\.env.local" }
        Write-Host "== Installing Python deps (uv) ==" -ForegroundColor Cyan
        Push-Location backend; uv sync --all-extras; Pop-Location
        Write-Host "== Installing Node deps (npm) ==" -ForegroundColor Cyan
        Push-Location frontend; npm install; Pop-Location
        Write-Host ""
        Write-Host "Setup complete. Run '.\tasks.ps1 dev-api' and '.\tasks.ps1 dev-frontend' to start." -ForegroundColor Green
    }
    "dev-api" {
        Push-Location backend
        uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        Pop-Location
    }
    "dev-frontend" {
        Push-Location frontend
        npm run dev
        Pop-Location
    }
    "test" {
        Write-Host "== Running Backend Tests ==" -ForegroundColor Cyan
        Push-Location backend; uv run pytest -v; Pop-Location
        Write-Host "== Running Frontend Tests ==" -ForegroundColor Cyan
        Push-Location frontend; npm run test:unit; Pop-Location
    }
    "test-backend" {
        Push-Location backend; uv run pytest -v; Pop-Location
    }
    "test-frontend" {
        Push-Location frontend; npm run test:unit; Pop-Location
    }
    "lint" {
        Write-Host "== Linting Backend ==" -ForegroundColor Cyan
        Push-Location backend; uv run ruff check .; Pop-Location
        Write-Host "== Linting Frontend ==" -ForegroundColor Cyan
        Push-Location frontend; npm run lint; Pop-Location
    }
    "format" {
        Push-Location backend; uv run ruff format .; Pop-Location
    }
    "format-check" {
        Push-Location backend; uv run ruff format --check .; Pop-Location
    }
    "build" {
        Write-Host "== Building Frontend ==" -ForegroundColor Cyan
        Push-Location frontend; npm run build; Pop-Location
    }
    "clean" {
        $dirs = @("backend\.venv", "frontend\node_modules", "frontend\.next", "frontend\out")
        foreach ($dir in $dirs) {
            if (Test-Path $dir) {
                Remove-Item -Recurse -Force $dir
                Write-Host "  Removed: $dir" -ForegroundColor DarkGray
            }
        }
        Write-Host "Cleaned." -ForegroundColor Green
    }
    # -- Versioning & Release --
    "version" {
        & .\scripts\new_version.ps1 @args
    }
    "release" {
        & .\scripts\new_release.ps1 @args
    }
    "help" {
        Write-Host ""
        Write-Host "  Travel AI World — Task Runner" -ForegroundColor Yellow
        Write-Host "  ────────────────────────────────────────" -ForegroundColor DarkGray
        Write-Host "  .\tasks.ps1 setup           First-time project setup"
        Write-Host "  .\tasks.ps1 dev-api         Run backend locally (hot-reload)"
        Write-Host "  .\tasks.ps1 dev-frontend    Run frontend locally (hot-reload)"
        Write-Host "  .\tasks.ps1 test            Run all tests (backend + frontend)"
        Write-Host "  .\tasks.ps1 test-backend    Backend tests only"
        Write-Host "  .\tasks.ps1 test-frontend   Frontend tests only"
        Write-Host "  .\tasks.ps1 lint            Lint backend + frontend"
        Write-Host "  .\tasks.ps1 format          Auto-format backend (ruff)"
        Write-Host "  .\tasks.ps1 format-check    Check formatting (CI)"
        Write-Host "  .\tasks.ps1 build           Build frontend for production"
        Write-Host "  .\tasks.ps1 clean           Remove caches and node_modules"
        Write-Host "  ────────────────────────────────────────" -ForegroundColor DarkGray
        Write-Host "  .\tasks.ps1 version         Bump version (patch, syncs all manifests)"
        Write-Host "    -Bump minor|major          Bump minor or major instead of patch"
        Write-Host "    -NoCommit                  Update files without committing"
        Write-Host "  .\tasks.ps1 release          Create GitHub Release (gh CLI)"
        Write-Host "    -PreRelease                Mark as pre-release"
        Write-Host "    -Draft                     Create as draft"
        Write-Host ""
    }
    default {
        Write-Host "Unknown task: '$Task'" -ForegroundColor Red
        & $PSCommandPath help
    }
}
