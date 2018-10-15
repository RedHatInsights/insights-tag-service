import datetime
from db.models import Tag
import factory
from insights_connexion.db import base
import insights_connexion.test.oatts as oatts


def seed():
    class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Tag
            sqlalchemy_session = base.session
            sqlalchemy_session_persistence = 'commit'

        id = 'default'
        name = 'default'
        description = 'This is the default tag.'
        value = 'default'
        created_at = datetime.datetime(2016, 11, 3)
        updated_at = datetime.datetime(2016, 11, 3)

    TagFactory()


oatts.seed = seed
oatts.test()
