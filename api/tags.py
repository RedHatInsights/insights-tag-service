import asyncio

from aiohttp.web import json_response
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

async def _delete_tag(id):
    async with db.transaction():
        existing_tag = await _get_one_tag(id)

        if existing_tag is None:
            return responses.not_found()

        await existing_tag.delete()
        return json_response(status=responses.delete())

async def search(page, page_size, sort_by, sort_dir, request=None):
    sort_func = getattr(db, sort_dir)
    [tags, count] = await asyncio.gather(
        Tag.query.limit(page_size).offset(
            page * page_size).order_by(sort_func(sort_by)).gino.all(),
        db.scalar(db.select([db.func.count(Tag.id)]))
    )

    tags_dump = [tag.dump() for tag in tags]
    return responses.search(count, tags_dump)


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


async def delete(id):
    return _delete_tag(id)