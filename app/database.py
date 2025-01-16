import asyncpg

DATABASE_URL = "postgresql://postgres:dani0919@localhost:5432/ReservationUpdateDb"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
