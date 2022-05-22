import uuid
import datetime

from app import db
from app.exception import DataExist
from app.main.model.user import User


class UserService:
    def save_new(self, data):
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            new_user = User(
                full_name=data['name'],
                username=data['username'],
                password=data['password'],
                is_doctor=data.get('is_doctor') or False
            )
            self.save_changes(new_user)
            return new_user
        else:
            raise DataExist(f"User with username {data['username']} is exists")

    def update(self, object, data):
        pass

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()