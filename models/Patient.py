from project import db

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    age = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    weight = db.Column(db.String(255))
    height = db.Column(db.String(255))
    currentillness = db.Column(db.String(255))
    profile_picture = db.Column(db.String(), nullable=True)
    price_package = db.Column(db.Integer)
    insurance_package = db.Column(db.Integer)