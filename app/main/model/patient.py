from app import db, flask_bcrypt

class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50))
    bod = db.Column(db.Date)
    no_ktp = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    vaccine_type = db.Column(db.String(255))
    vaccine_count = db.Column(db.Integer)


    def __repr__(self):
        return "<Patient '{}'>".format(self.full_name)