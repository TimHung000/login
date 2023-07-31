import asyncpg
from src.config import get_settings

class Database:
    def __init__(self):
        self.db_conn_pool: syncpg.pool.Pool

    async def create_db_conn_pool(self):
        settings = get_settings()
        try:
            self.db_conn_pool = await asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                min_size = 5,
                max_size = 10
            )
            print("Database pool connectionn opened")
        except Exception as e:
            print(f"Error creating database connection pool: {e}")

    async def close_db_conn_pool(self):
        if self.db_conn_pool:
            try:
                await self.db_conn_pool.close()

                print("Database pool connection closed")
            except Exception as e:
                print(f"Error closing database connection pool: {e}")

database = Database()