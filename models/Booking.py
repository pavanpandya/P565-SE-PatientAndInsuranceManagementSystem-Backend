from project import db

class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    fees = db.Column(db.Integer)
    date = db.Column(db.Date)
    status = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    feedback = db.Column(db.String(255))
    