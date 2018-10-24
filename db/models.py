from insights_connexion.db.gino import db


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Unicode, primary_key=True)
    name = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    value = db.Column(db.Unicode)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,
                           onupdate=db.func.now(),
                           server_default=db.func.now())

    def dump(self):
        return {k: v for k, v in self.__values__.items() if v is not None}
