import uuid
import datetime, dateparser

from app import db
from app.exception import DataExist, DataNotFound
from app.main.model.doctor import Doctor



class DoctorService:
    def save_new(self, user, data):
        doctor = Doctor.query.filter_by(user=user).first()
        if not doctor:
            new_doctor = Doctor(
                full_name=data['name'],
                gender=data['gender'],
                bod=data['birthdate'],
                work_start_time=dateparser.parse(data['work_start_time']).time(),
                work_end_time=dateparser.parse(data['work_end_time']).time(),
            )
            self.save_changes(new_doctor)
            return new_doctor
        else:
            raise DataExist(f"Doctor is exists")

    def update(self, object, data):
        object.full_name = data['name']
        object.gender = data['gender']
        object.bod = dateparser.parse(data['birthdate'])
        object.work_start_time = dateparser.parse(data['work_start_time']).time()
        object.work_end_time = dateparser.parse(data['work_end_time']).time()
        self.save_changes(object)

    def get_all(self, **kwargs):
        return Doctor.query.filter_by(**kwargs)

    def get_by_id(self, id):
        employee = Doctor.query.filter_by(id=id).first()
        if not employee:
            raise DataNotFound(f"Doctor with id :{id} not found !!")
        return employee

    def delete(self, id):
        Doctor.query.filter_by(id=id).delete()
        db.session.commit()

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()