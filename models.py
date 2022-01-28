from app import db

class CrestoPass(db.Model):
    __tablename__ = 'cresto_passes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.String())
    owner_id = db.Column(db.String())
    image = db.Column(db.String())
    description = db.Column(db.String())
    mintedAt = db.Column(db.DateTime())

    def __init__(self, id, name, category, owner_id, image, description, mintedAt):
        self.id = id
        self.name = name
        self.category = category
        self.owner_id = owner_id
        self.image = image
        self.description = description
        self.mintedAt = mintedAt

    def __repr__(self):
        return '<id {}> <name {}> <category {}> <mintedAt {}'.format(self.id, self.name, self.category, self.mintedAt)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
