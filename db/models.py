from db.base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    value = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(),
                        server_default=func.now())

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_') and v is not None])
