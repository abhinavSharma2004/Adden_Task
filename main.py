from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine
import models
import controller 

async def create_database_tables():
    """Create all tables asynchronously."""
    print("Creating database tables...")

    # creating tables from defined model
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")

@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_database_tables()
    yield

# lifespan as the lifecycle handler.
app = FastAPI(lifespan=lifespan)

app.include_router(controller.router)