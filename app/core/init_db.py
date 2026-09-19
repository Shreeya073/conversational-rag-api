import asyncio

from app.core.database import create_database, engine
from app.models.booking import Base

async def create_tables() -> None:
   
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def main() -> None:

    await create_database()
    await create_tables()

    await engine.dispose()

    print("Database and tables created successfully.")

if __name__ == "__main__":
    asyncio.run(main())