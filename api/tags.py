from connexion import request
from db.base import session
from db.models import Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError


def search():
    tags = session.query(Tag).all()
    tags_dump = [tag.dump() for tag in tags]
    return {'count': 0, 'results': tags_dump}


def post():
    try:
        new_tag = Tag(id=request.json['id'], name=request.json['name'],
                      description=request.json['description'])
        session.add(new_tag)
        session.commit()
        response_body = session.query(Tag).filter(
            Tag.id == request.json['id']).one()
    except (IntegrityError):
        return 'Exists', HTTPStatus.CONFLICT

    return response_body.dump(), HTTPStatus.CREATED


def get(id):
    return session.query(Tag).filter(Tag.id == id).one().dump()


def put():
    pass


def patch():
    pass


def delete():
    pass
