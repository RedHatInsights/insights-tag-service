from connexion import request
from db.base import session
from db.models import Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError


def search():
    return 'test', 200


def post():
    try:
        new_tag = Tag(id=request.json['id'], name=request.json['name'],
                      description=request.json['description'])
        session.add(new_tag)
        # response_body = session.query(Tag).filter_by(id=request.json['id'])
        session.commit()
    except (IntegrityError):
        return 'Exists', HTTPStatus.CONFLICT

    return (), HTTPStatus.CREATED


def get(id):
    return 'test', 200


def put():
    pass


def patch():
    pass


def delete():
    pass
