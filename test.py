import datetime
from db.models import Tag
import factory
import insights_connexion.test.oatts as oatts


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    id = 'default'
    name = 'default'
    description = 'This is the default tag.'
    value = 'default'
    created_at = datetime.datetime(2016, 11, 3)
    updated_at = datetime.datetime(2016, 11, 3)


async def seed():
    return (await TagFactory().create(),
            await TagFactory(id='put-tag').create(),
            await TagFactory(id='get-tag').create(),
            await TagFactory(id='delete-tag').create(),
            await TagFactory(id='patch-tag').create())


oatts.seed = seed
oatts.test()
