from gino import Gino
from gino.schema import GinoSchemaVisitor

from config import POSTGRESQL_URL

db = Gino()


async def create_db():
    db.gino: GinoSchemaVisitor
    await db.set_bind(POSTGRESQL_URL)
    # await db.set_bind("postgresql://postgres:copium1158@194.15.113.81:5432/sova")
    await db.gino.create_all()


async def drop_connection():
    await db.pop_bind().close()

