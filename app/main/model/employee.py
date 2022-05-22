from app import db, flask_bcrypt
from sqlalchemy.orm import relationship

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50))
    bod = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="employee")

    def __repr__(self):
        return "<Employee '{}'>".format(self.full_name)