from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specie_id = db.Column(db.Integer, db.ForeignKey("specie.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    favorites = db.relationship("Favorite", backref="character", lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specie_id": self.specie_id,
            "planet_id": self.planet_id
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    clima = db.Column(db.String(100), nullable=False)
    characters = db.relationship("Character", backref="planet", lazy=True)
    favorites = db.relationship("Favorite", backref="planet", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clima": self.clima
        }
    
class Specie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    characters = db.relationship("Character", backref="specie", lazy=True)
    favorites = db.relationship("Favorite", backref="specie", lazy=True)

    def __repr__(self):
        return '<Specie %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.planet_id
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable = True)
    specie_id = db.Column(db.Integer, db.ForeignKey("specie.id"), nullable = True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable = True)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "specie_id": self.specie_id,
            "character_id": self.character_id
        }
