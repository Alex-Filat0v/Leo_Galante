import asyncpg
from passlib.context import CryptContext
import uuid
import datetime
import logging

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user='postgres',  # Укажите ваши данные
            password='1234',
            database='karno',  # Имя базы данных для PostgreSQL
            host="localhost",
            port="5432"
        )
        await self._create_tables()

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id UUID PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    created_at TIMESTAMP DEFAULT NOW(),
                    expires_at TIMESTAMP
                );
            """)

    async def create_user(self, username: str, password: str):
        hashed_password = pwd_context.hash(password)
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO users (username, password) VALUES ($1, $2)",
                    username, hashed_password
                )
                return True
        except asyncpg.UniqueViolationError:
            return False

    async def get_user(self, username: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1", username
            )

    async def get_user_by_id(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )

    async def verify_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user:
            return False
        return pwd_context.verify(password, user['password'])

    async def create_session(self, user_id: int):
        session_id = uuid.uuid4()
        expires_at = datetime.datetime.now() + datetime.timedelta(days=7)
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO sessions (session_id, user_id, expires_at) VALUES ($1, $2, $3)",
                session_id, user_id, expires_at
            )
        return session_id

    async def get_session(self, session_id: str):
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            return None

        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM sessions WHERE session_id = $1 AND expires_at > NOW()",
                session_uuid
            )

    async def delete_session(self, session_id: str):
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            return

        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM sessions WHERE session_id = $1",
                session_uuid
            )

    async def change_password(self, username: str, new_password: str):
        hashed_password = pwd_context.hash(new_password)
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET password = $1 WHERE username = $2",
                hashed_password, username
            )


db = Database()
