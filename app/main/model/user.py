from app import db, flask_bcrypt
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    is_doctor = db.Column(db.Boolean)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    doctor = relationship("Doctor", back_populates="user")
    employee = relationship("Employee", back_populates="user")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)