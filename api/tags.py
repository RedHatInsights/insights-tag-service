from connexion import request
from insights_connexion import responses
from insights_connexion.db.base import session
from db.models import Tag


def _get_one_tag(id):
    return session.query(Tag).filter(Tag.id == id).one()


def _update_tag(id):
    existing_tag = session.query(Tag).filter(Tag.id == id).first()

    if existing_tag is None:
        return responses.not_found()

    existing_tag.update(**request.json)
    session.commit()
    return responses.update(_get_one_tag(id).dump())


def search():
    tags = session.query(Tag).all()
    tags_dump = [tag.dump() for tag in tags]
    return responses.search(0, tags_dump)


def post():
    new_tag = Tag(**request.json)
    session.add(new_tag)
    session.commit()
    response_body = _get_one_tag(request.json['id'])
    return responses.create(response_body.dump())


def get(id):
    return _get_one_tag(id).dump()


def put(id):
    return _update_tag(id)


def patch(id):
    return _update_tag(id)


def delete(id):
    existing_tag = _get_one_tag(id)
    if existing_tag is None:
        return responses.not_found()

    session.delete(existing_tag)
    return responses.delete()
