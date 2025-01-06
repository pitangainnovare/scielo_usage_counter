from app.declararive import Base
from sqlalchemy import create_engine


def get_session():
    ...

def create_tables(str_connection):
    engine = create_engine(str_connection)
    Base.metadata.create_all(engine)
