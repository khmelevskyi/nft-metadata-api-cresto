from app import db

class CrestoPass(db.Model):
    __tablename__ = 'cresto_passes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    symbol = db.Column(db.String())
    owner_id = db.Column(db.String())
    image = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, id, name, symbol, owner_id, image, description):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.owner_id = owner_id
        self.image = image
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
