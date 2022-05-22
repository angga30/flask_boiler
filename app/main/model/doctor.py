from app import db, flask_bcrypt
from sqlalchemy.orm import relationship

class Doctor(db.Model):
    __tablename__ = "doctor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.String(50))
    bod = db.Column(db.Date)
    work_start_time = db.Column(db.Time)
    work_end_time = db.Column(db.Time)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="doctor")

    appointments = relationship("Appointment")

    def __repr__(self):
        return "<Doctor '{}'>".format(self.full_name)