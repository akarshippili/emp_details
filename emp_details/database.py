from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:akarsh@localhost:5432/employee'
SQLALCHEMY_DATABASE_URL = 'sqlite:///employee.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import emp_details.models
    Base.metadata.create_all(bind=engine)
