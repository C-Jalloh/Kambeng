import os
import sys
import shutil
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("HEXAI_WEBHOOK_SECRET", "test-webhook-secret")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./kambeng_test.db")
os.environ.setdefault("MEDIA_ROOT", "media_test")
os.environ.setdefault("STORAGE_STRATEGY", "local")

from app.db.database import Base, get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402
from app import models as _models  # noqa: F401,E402


@pytest.fixture(scope="session")
def integration_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


@pytest.fixture(scope="session", autouse=True)
def cleanup_integration_engine(request, integration_engine):
    def _finalizer():
        import asyncio

        asyncio.run(integration_engine.dispose())

    request.addfinalizer(_finalizer)


@pytest.fixture(scope="session")
def integration_session_factory(integration_engine):
    return async_sessionmaker(integration_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_integration_db(integration_engine):
    async with integration_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with integration_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
def cleanup_media_root():
    media_root = Path(os.environ.get("MEDIA_ROOT", "media_test"))
    if media_root.exists():
        shutil.rmtree(media_root)
    yield
    if media_root.exists():
        shutil.rmtree(media_root)


@pytest.fixture
def client(integration_session_factory):
    async def _override_get_db():
        async with integration_session_factory() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = _override_get_db

    class _ResponseProxy:
        """Wrap a sync Response but also support awaiting to run the same
        request in a thread and return a real Response for async tests.
        """

        def __init__(self, sync_response, async_call):
            self._sync = sync_response
            self._async_call = async_call

        def __getattr__(self, item):
            return getattr(self._sync, item)

        def json(self, *args, **kwargs):
            return self._sync.json(*args, **kwargs)

        def text(self):
            return self._sync.text

        def __await__(self):
            import asyncio

            return asyncio.to_thread(self._async_call).__await__()


    class AsyncableTestClient:
        """Wrap a sync TestClient but provide methods that return a
        `._ResponseProxy` which is usable synchronously and awaitable.
        """

        def __init__(self, test_client: TestClient):
            self._client = test_client

        def __getattr__(self, name):
            return getattr(self._client, name)

        def _make_proxy(self, method_name, *args, **kwargs):
            sync_method = getattr(self._client, method_name)
            # Perform sync call immediately for sync tests
            sync_resp = sync_method(*args, **kwargs)

            # Prepare async callable to run the same request in a thread
            def async_call():
                return sync_method(*args, **kwargs)

            return _ResponseProxy(sync_resp, async_call)

        def get(self, *args, **kwargs):
            return self._make_proxy("get", *args, **kwargs)

        def post(self, *args, **kwargs):
            return self._make_proxy("post", *args, **kwargs)

        def put(self, *args, **kwargs):
            return self._make_proxy("put", *args, **kwargs)

        def delete(self, *args, **kwargs):
            return self._make_proxy("delete", *args, **kwargs)

        def patch(self, *args, **kwargs):
            return self._make_proxy("patch", *args, **kwargs)

    with TestClient(fastapi_app) as test_client:
        yield AsyncableTestClient(test_client)
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def integration_db_session(integration_session_factory):
    async def _get_session():
        async with integration_session_factory() as session:
            return session

    return _get_session


@pytest_asyncio.fixture
async def db_session(integration_session_factory):
    """Provide an async DB session instance for tests that expect `db_session`."""
    async with integration_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(integration_session_factory):
    """Async HTTP client for tests marked with asyncio.

    Ensures the FastAPI `get_db` dependency is overridden to use the
    integration session factory so requests see the in-memory DB.
    """

    async def _override_get_db():
        async with integration_session_factory() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(app=fastapi_app, base_url="http://testserver") as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    def _auth_headers(wave_number: str, password: str):
        response = client.post(
            "/api/auth/login",
            data={"username": wave_number, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200
        payload = response.json()
        token = payload.get("access_token") or payload.get("data", {}).get("tokens", {}).get("accessToken")
        assert token, f"No access token found in login response: {payload}"
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers


@pytest_asyncio.fixture
async def sample_campaign(db_session):
    """Create a simple campaign and return it."""
    from app.models.user import User
    from app.models.campaign import Campaign, CampaignMode

    user = User(full_name="Sample User", email="sample@example.com", wave_number="+2207000991", password_hash="x")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    campaign = Campaign(user_id=user.id, title="Sample Campaign", slug="sample-campaign", description="", mode=CampaignMode.ONGOING)
    db_session.add(campaign)
    await db_session.commit()
    await db_session.refresh(campaign)
    return campaign


@pytest_asyncio.fixture
async def sample_campaign_with_alias(db_session):
    from app.models.user import User
    from app.models.campaign import Campaign, CampaignMode
    from app.models.alias import CampaignAlias

    user = User(full_name="Alias User", email="alias-user@example.com", wave_number="+2207000992", password_hash="x")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    campaign = Campaign(user_id=user.id, title="Alias Campaign", slug="alias-campaign", description="", mode=CampaignMode.ONGOING)
    db_session.add(campaign)
    await db_session.commit()
    await db_session.refresh(campaign)

    alias = CampaignAlias(campaign_id=campaign.id, short_code="alias123")
    db_session.add(alias)
    await db_session.commit()
    await db_session.refresh(alias)

    return campaign, alias
