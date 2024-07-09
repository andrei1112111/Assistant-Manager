from .connect_db import connect_db, disconnect_db
import atexit

connect_db()

atexit.register(disconnect_db)

__all__ = [
    "connect_db",
    "disconnect_db",
]
