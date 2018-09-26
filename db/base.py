import common.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def init():
    engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format(config.DATABASE.USER, config.DATABASE.PASSWORD,
                                             config.DATABASE.HOST, config.DATABASE.PORT, config.DATABASE.NAME),
        pool_size=config.DB_POOL_SIZE,
        max_overflow=config.DB_MAX_OVERFLOW)
    session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    Base.query = session.query_property()
    Base.metadata.create_all(engine)
    return session


session = init()
