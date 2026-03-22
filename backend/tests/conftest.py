from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.db.session import get_db
from app.models.base import Base  # Fix #8: import from shared base module

# Test database URL (using SQLite in-memory for speed/isolation in tests)
TEST_SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_SQLALCHEMY_DATABASE_URI)
AsyncSessionTest = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionTest() as session:
        yield session

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    # Override get_db dependency
    async def _get_test_db():
        yield db_session
        
    app.dependency_overrides[get_db] = _get_test_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()
