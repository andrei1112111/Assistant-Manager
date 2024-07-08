from sqlalchemy.orm import sessionmaker

from .db import engine

bd_session = sessionmaker(bind=engine)
