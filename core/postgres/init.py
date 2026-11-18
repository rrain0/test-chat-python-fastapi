from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config.env import POSTGRES_URL



class FastAPIPostgres:
    def __init__(self, app: FastAPI, database_url: str = POSTGRES_URL):
        self.app = app
        self.engine = create_async_engine(database_url, echo=True)

    def lifespan(self):
        """Attaches the DB setup and teardown sequence directly to the app."""
        # Save the engine into app.state so dependencies can safely reference it
        self.app.state.postgres_engine = self.engine

        # Wrap the original application lifespan handler if one exists
        original_lifespan = self.app.router.lifespan_context

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):
            # CURRENT LIFESPAN
            # --- STARTUP CODE ---
            # Run structural creations asynchronously
            print('Initializing database tables...')
            # Печатает в консоль список таблиц, которые SQLModel видит в памяти
            print('Registered tables found:', SQLModel.metadata.tables.keys())

            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)


            # NESTED LIFESPAN
            # Yield control over to any existing lifespan handlers or endpoints
            async with original_lifespan(app) as maybe_state:
                yield maybe_state


            # CURRENT LIFESPAN
            # --- SHUTDOWN CODE ---
            print('Closing database connections...')
            await self.engine.dispose()

        # Re-assign the app's router lifespan context dynamically
        self.app.router.lifespan_context = combined_lifespan
        return self



def init_postgres(app: FastAPI):
    FastAPIPostgres(app).lifespan()



# This dependency extracts the engine from the app state and yields a session
async def get_postgres_session(request: Request):
    # Retrieve the engine attached during the lifespan setup
    engine = request.app.state.postgres_engine

    # Yield the session to the route, ensuring it cleanly closes afterward
    async with AsyncSession(engine) as session:
        session.sync_session.expire_on_commit = False
        yield session


AsyncPostgresDep = Annotated[AsyncSession, Depends(get_postgres_session)]
