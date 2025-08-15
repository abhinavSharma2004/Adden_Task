from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://marketing_user:your_password@localhost/marketing_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# async_sessionmaker for asynchronous sessions
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use AsyncAttrs for declarative base in an async context
Base = declarative_base(cls=AsyncAttrs)

# creating a session for any db operations
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
