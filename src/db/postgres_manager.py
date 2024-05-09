import os
import asyncpg
from dotenv import load_dotenv
from databases import Database


load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


async def connect_to_database():
    database = Database(DATABASE_URL)
    await database.connect()
    return database


async def disconnect_from_database(database: Database):
    await database.disconnect()


async def get_db():
    return await connect_to_database()