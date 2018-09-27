import factory
from db import models
from db import base
import datetime


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Tag
        sqlalchemy_session = base.session
        sqlalchemy_session_persistence = 'commit'

    id = 'default'
    name = 'default'
    description = 'This is the default tag.'
    value = 'default'
    created_at = datetime.datetime(2016, 11, 3)
    updated_at = datetime.datetime(2016, 11, 3)
