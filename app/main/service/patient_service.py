import uuid
import datetime, dateparser

from app import db
from app.exception import DataExist, DataNotFound
from app.main.model.patient import Patient



class PatientService:
    def save_new(self, data):
        patient = Patient.query.filter_by(no_ktp=data["no_ktp"]).first()
        if not patient:
            new_patient = Patient(
                full_name=data['name'],
                gender=data['gender'],
                bod=data['birthdate'],
                address=data['address'],
                no_ktp=data['no_ktp']
            )
            self.save_changes(new_patient)
            return new_patient
        else:
            raise DataExist(f"Patient with no_ktp {data['no_ktp']} is exists")

    def update(self, object, data):
        object.full_name = data['name']
        object.gender = data['gender']
        object.bod = dateparser.parse(data['birthdate'])
        object.address = data['address']
        object.no_ktp = data['no_ktp']
        object.vaccine_type = data.get('vaccine_type')
        object.vaccine_count = data.get('vaccine_count')
        self.save_changes(object)

    def get_all(self, **kwargs):
        return Patient.query.filter_by(**kwargs)

    def get_by_id(self, **kwargs):
        patient = Patient.query.filter_by(**kwargs).first()
        if not patient:
            raise DataNotFound(f"Patient with filter :{kwargs} not found !!")
        return patient

    def delete(self, id):
        Patient.query.filter_by(id=id).delete()
        db.session.commit()

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()