# 🇬🇧 English

## Test Setup (`tests/`)

This Template includes a robust test suite using **Pytest** and **Pytest-Asyncio**. The main strength of this setup is that _it can run without needing perfectly running PostgreSQL instance_.

### Test Environment

To ensure the tests are fast, clean, and don't destroy your development environment, take a look at `tests/conftest.py`:

1. **In-Memory Database**: By default, the tests override the database injection (`get_db`) and use an async in-memory SQLite (`aiosqlite`).
2. **Automated Setup and Teardown**: Each test execution reconstructs the database schema, guaranteeing an entirely pristine state before each test.

### Useful Commands

The CI/CD pipeline is ready to reject unstable code. Verify your code beforehand with these quick commands:

#### Run all Tests

```bash
uv run pytest -v
```

#### Check Coverage

To know exactly which lines of your code are **NOT** being executed by the tests, run:

```bash
uv run pytest -v --cov=app --cov-report=term-missing
```

This will print a table indicating which files lack tests and precisely on which lines.

#### Run Specific Tests

Focus on a single test to save time during development:

```bash
uv run pytest tests/api/test_users.py::test_create_user -v
```

---

### Writing New Tests

When adding new features, follow the general pattern:

1. Create a new file in `tests/api/` with the prefix `test_*.py`.
2. Test functions must start with `test_` and must be async (`async def test_create_item()`) thanks to the config in `pyproject.toml` (`asyncio_mode = "auto"`).
3. Use the `client: AsyncClient` fixture as a dependency in your test functions to properly emulate API calls.

---

# 🇪🇸 Español

## Configuración de Tests (`tests/`)

Este Template incluye una suite de pruebas robusta usando **Pytest** y **Pytest-Asyncio**. La fortaleza principal de este setup es que _puede correr sin necesidad de levantar un PostgreSQL real_.

### Entorno de Pruebas

Para garantizar que los tests sean rápidos, limpios y no destruyan tu entorno de desarrollo, echa un vistazo a `tests/conftest.py`:

1. **Base de Datos en Memoria**: Por defecto, los tests sobrescriben la inyección de la base de datos (`get_db`) y utilizan SQLite asíncrono en memoria (`aiosqlite`).
2. **Setup y Teardown Automatizado**: Cada ejecución de test reconstruye el esquema de la base de datos, garantizando que el estado sea prístino antes de cada test.

### Comandos Útiles

El pipeline de CI/CD está preparado para rechazar código inestable. Verifica tu código antes con estos comandos rápidos:

#### Correr todos los Tests

```bash
uv run pytest -v
```

#### Comprobar la Cobertura (Coverage)

Para saber qué líneas específicas de tu código **NO** están siendo ejecutadas por los tests, corre:

```bash
uv run pytest -v --cov=app --cov-report=term-missing
```

Esto imprimirá una tabla indicando qué archivos carecen de tests y en qué números de línea específicos.

#### Correr Tests Específicos

Enfocarte de un solo test para ahorrar tiempo mientras desarrollas:

```bash
uv run pytest tests/api/test_users.py::test_create_user -v
```

---

### Escribiendo Nuevos Tests

Al añadir nuevas funcionalidades, sigue el patrón general:

1. Crea un nuevo archivo en `tests/api/` con el prefijo `test_*.py`.
2. Las funciones de test deben empezar por `test_` y deben ser asíncronas (`async def test_crear_item()`) gracias a la configuración en `pyproject.toml` (`asyncio_mode = "auto"`).
3. Utiliza la fixture `client: AsyncClient` como dependencia en tus funciones de test para emular llamadas a la API limpiamente.
