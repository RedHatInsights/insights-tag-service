import asyncio

from db.models import Tag
from insights_connexion import responses
from insights_connexion.db.gino import db


async def _get_one_tag(id):
    return await Tag.query.where(Tag.id == id).gino.first()


async def _update_tag(id, body):
    async with db.transaction():
        existing_tag = await _get_one_tag(id)

        if existing_tag is None:
            return responses.not_found()

        await existing_tag.update(**body).apply()
        updated_tag = await _get_one_tag(id)
        return responses.update(updated_tag.dump())


async def search(request=None):
    [tags, count] = await asyncio.gather(
        Tag.query.gino.all(),
        db.scalar(db.select([db.func.count(Tag.id)]))
    )

    namespaces_data = {}
    for tag in tags:
        if tag.namespace not in namespaces_data:
            namespaces_data[tag.namespace] = []
        namespaces_data[tag.namespace].append({tag.name: tag.value})

    return responses.get(namespaces_data)


async def post(request=None):
    async with db.transaction():
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
