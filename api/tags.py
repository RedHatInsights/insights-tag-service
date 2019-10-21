import asyncio

from db.models import Tag
from insights_connexion import responses
from insights_connexion.db.gino import db
from sqlalchemy import and_


async def _get_one_tag(id):
    return await Tag.query.where(Tag.id == id).gino.first()

async def _get_duplicate_tag(account_id, namespace, name, value):
    tags = await Tag.query.where(and_(Tag.account_id == account_id, Tag.namespace == namespace, Tag.name == name, Tag.value == value)).gino.all()
    return await Tag.query.where(and_(Tag.account_id == account_id, Tag.namespace == namespace, Tag.name == name, Tag.value == value)).gino.first()

async def _update_tag(id, body):
    async with db.transaction():
        existing_tag = await _get_one_tag(id)

        if existing_tag is None:
            return responses.not_found()

        tag_to_create = Tag(**body)

        duplicate_tag = await _get_duplicate_tag(tag_to_create.account_id, tag_to_create.namespace, tag_to_create.name, tag_to_create.value)
        if duplicate_tag is not None:
            return responses.resource_exists('Tag exists; aborted to avoid duplication.')

        await existing_tag.update(**body).apply()
        updated_tag = await _get_one_tag(id)
        return responses.update(updated_tag.dump())


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
        # Wait to see if a duplicate exists
        duplicate_tag = await _get_duplicate_tag(tag_to_create.account_id, tag_to_create.namespace, tag_to_create.name, tag_to_create.value)
        if duplicate_tag is None:
            created_tag = await tag_to_create.create()
            return responses.create(created_tag.dump())
        else:
            return responses.resource_exists('Tag exists; aborted to avoid duplication.')


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
