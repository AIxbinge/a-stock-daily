"""数据库配置"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import redis.asyncio as redis

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    database_url: str = "postgresql+asyncpg://stockuser:stockpass@localhost:5432/stockdb"
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()

# 异步数据库引擎
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 基础模型
Base = declarative_base()


async def init_db():
    """初始化数据库连接"""
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()


# Redis 客户端
redis_client: redis.Redis = None


async def get_redis() -> redis.Redis:
    """获取 Redis 客户端"""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    return redis_client


async def close_redis():
    """关闭 Redis 连接"""
    global redis_client
    if redis_client:
        await redis_client.close()
