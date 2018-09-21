from db.base import Base
from sqlalchemy import Column, String


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    value = Column(String)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_') and v is not None])
