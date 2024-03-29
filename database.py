from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    status = db.Column(db.String(100))
    species = db.Column(db.String(100))
    type = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    origin_name = db.Column(db.String(100))
    location_name = db.Column(db.String(100))
    image = db.Column(db.String(500))
