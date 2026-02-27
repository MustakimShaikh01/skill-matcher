from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# ─── MongoDB ───────────────────────────────────────────────────────────────────
mongo_client: AsyncIOMotorClient = None
mongo_db = None


async def connect_mongodb():
    global mongo_client, mongo_db
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongo_db = mongo_client.skillmatch
        await mongo_client.admin.command("ping")
        logger.info("✅ MongoDB connected")
    except Exception as e:
        logger.warning(f"⚠️  MongoDB not available: {e}. Using in-memory store.")
        mongo_db = None


async def close_mongodb():
    global mongo_client
    if mongo_client:
        mongo_client.close()


def get_mongo_db():
    return mongo_db


# ─── PostgreSQL ────────────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# Use sync-compatible URL for SQLAlchemy ORM models (for metadata)
pg_engine = None
AsyncSessionLocal = None


async def connect_postgres():
    global pg_engine, AsyncSessionLocal
    try:
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        pg_engine = create_async_engine(db_url, echo=False, pool_pre_ping=True)
        AsyncSessionLocal = sessionmaker(
            pg_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with pg_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ PostgreSQL connected")
    except Exception as e:
        logger.warning(f"⚠️  PostgreSQL not available: {e}. Using in-memory store.")
        pg_engine = None


async def close_postgres():
    global pg_engine
    if pg_engine:
        await pg_engine.dispose()


async def get_db():
    if AsyncSessionLocal is None:
        yield None
        return
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
