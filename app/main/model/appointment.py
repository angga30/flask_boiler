from app import db, flask_bcrypt
from sqlalchemy.orm import relationship

import enum
from sqlalchemy import Enum

class Appointment(db.Model):
    __tablename__ = "appointement"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", back_populates="appointments")

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patient = relationship("Patient", back_populates="appointments")

    status = db.Column(db.String(50))
    diagnose = db.Column(db.Text)
    notes = db.Column(db.Text)
    appointment_time = db.Column(db.DateTime)


    def __repr__(self):
        return "<Appointment '{}'>".format(self.patient.full_name)