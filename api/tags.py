from db.models import Tag
from insights_connexion import responses


async def _get_one_tag(id):
    return await Tag.query.where(Tag.id == id).gino.first()


async def _update_tag(id, body):
    existing_tag = await _get_one_tag(id)

    if existing_tag is None:
        return responses.not_found()

    await existing_tag.update(**body).apply()
    updated_tag = await _get_one_tag(id)
    return responses.update(updated_tag.dump())


async def search():
    tags = await Tag.query.gino.all()
    tags_dump = [tag.dump() for tag in tags]
    return responses.search(0, tags_dump)


async def post(request=None):
    body = await request.json()
    tag_to_create = Tag(**body)
    created_tag = await tag_to_create.create()
    return responses.create(created_tag.dump())


async def get(id):
    body = await _get_one_tag(id)
    if body is None:
        return responses.not_found()
    else:
        return responses.get(body.dump())


async def put(id, request=None):
    body = await request.json()
    return _update_tag(id, body)


async def patch(id, request=None):
    body = await request.json()
    return _update_tag(id, body)
