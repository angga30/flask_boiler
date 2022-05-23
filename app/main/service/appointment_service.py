import uuid
import datetime, dateparser

from sqlalchemy import extract

from app import db
from app.exception import DataExist, DataNotFound
from app.main.model.appointment import Appointment



class AppointmentService:
    def save_new(self, data):
        appointment_time = dateparser.parse(data['datetime'])

        appointment = Appointment.query.filter(
            extract('month', Appointment.appointment_time) == appointment_time.month,
            extract('year', Appointment.appointment_time) == appointment_time.year,
            extract('day', Appointment.appointment_time) == appointment_time.day,
            extract('hour', Appointment.appointment_time) == appointment_time.hour,
            Appointment.patient_id == data['patient_id'],
            Appointment.doctor_id == data['doctor_id']
        ).first()
        if not appointment:
            new_appointment = Appointment(
                doctor_id=data['doctor_id'],
                patient_id=data['patient_id'],
                status=data['status'],
                appointment_time=appointment_time,
            )
            self.save_changes(new_appointment)
            return new_appointment
        else:
            raise DataExist(f"Appointment with patient {appointment.patient.full_name} on {appointment.appointment_time} is exists")

    def update(self, object, data):
        object.docter_id = data['doctor_id']
        object.patient_id = data['patient_id']
        object.appointment_time = dateparser.parse(data['datetime'])
        object.status = data['status']
        object.diagnose = data.get('diagnose')
        object.notes = data.get('notes')
        self.save_changes(object)

    def get_all(self, **kwargs):
        return Appointment.query.filter_by(**kwargs)

    def get_filter_data(self, *args):
        return Appointment.query.filter(*args)

    def get_by_id(self, **kwargs):
        appointment = Appointment.query.filter_by(**kwargs).first()
        if not appointment:
            raise DataNotFound(f"Appointment with filter :{kwargs} not found !!")
        return appointment

    def delete(self, id):
        Appointment.query.filter_by(id=id).delete()
        db.session.commit()

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()