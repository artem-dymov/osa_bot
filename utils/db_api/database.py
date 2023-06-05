from gino import Gino
from gino.schema import GinoSchemaVisitor

from config import DATABASE_URL

db = Gino()


async def create_db():
    db.gino: GinoSchemaVisitor
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()


async def drop_connection():
    await db.pop_bind().close()

