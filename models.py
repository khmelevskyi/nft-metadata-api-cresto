from app import db

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
