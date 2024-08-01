from .load_b64Image import load_b64Image
from .storage import Storage

storage = Storage()

__all__ = [
    "load_b64Image",
    "storage"
]
