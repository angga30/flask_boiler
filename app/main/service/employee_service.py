import uuid
import datetime
import dateparser

from app import db
from app.exception import DataNotFound, DataExist
from app.main.model.employee import Employee


class EmployeeService:
    def save_new(self, user, data):
        employee = Employee.query.filter_by(user_id=user.id).first()
        if not employee:
            new_employee = Employee(
                full_name=data['name'],
                gender=data['gender'],
                bod=dateparser.parse(data['birthdate'])
            )
            self.save_changes(new_employee)
            return new_employee
        else:
            raise DataExist(f"Employee is exists")

    def update(self, object, data):
        object.full_name = data['name']
        object.gender = data['gender']
        object.bod = dateparser.parse(data['birthdate'])
        self.save_changes(object)

    def get_all(self, **kwargs):
        return Employee.query.filter_by(**kwargs)

    def get_by_id(self, id):
        employee = Employee.query.filter_by(id=id).first()
        if not employee:
            raise DataNotFound(f"Employee with id :{id} not found !!")
        return employee

    def delete(self, id):
        Employee.query.filter_by(id=id).delete()
        db.session.commit()

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()