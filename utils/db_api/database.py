from gino import Gino
from gino.schema import GinoSchemaVisitor

db = Gino()


async def create_db():
    db.gino: GinoSchemaVisitor
    await db.set_bind("postgresql://postgres:4334@localhost/sova-dev-ubuntu")
    # await db.set_bind("postgresql://postgres:copium1158@194.15.113.81:5432/sova")
    await db.gino.create_all()


async def drop_connection():
    await db.pop_bind().close()

