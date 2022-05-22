import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.exception import DataNotFound, CreateDataFailed, DataExist
from app.main.service.doctor_service import DoctorService
from app.main.service.user_service import UserService

from flask_expects_json import expects_json


schema = {
    "type": "object",
    "properties": {
        "username": { "type": "string" },
        "name": { "type": "string" },
        "password": { "type": "string" },
        "gender": { "type": "string" },
        "birthdate": { "type": "string" },
        "work_start_time": { "type": "string" },
        "work_end_time": { "type": "string" },
      },
    "required": ["username", "password", "birthdate", "work_start_time", "work_end_time"]
}



class DoctorView(MethodView):
    service = DoctorService()
    def get(self, id=None):
        if not id:
            doctors = self.service.get_all()
            res = []
            for doctor in doctors:
                res.append({
                    'id': doctor.id,
                    'name': doctor.full_name,
                    'gender': doctor.gender,
                    'birthdate': doctor.bod,
                    'work_start_time': doctor.work_start_time.isoformat(),
                    'work_end_time': doctor.work_end_time.isoformat(),
                })
        else:
            try:
                doctor = self.service.get_by_id(id)
                res = {
                    'id': doctor.id,
                    'name': doctor.full_name,
                    'gender': doctor.gender,
                    'birthdate': doctor.bod,
                    'work_start_time': doctor.work_start_time.isoformat(),
                    'work_end_time': doctor.work_end_time.isoformat(),
                }
            except DataNotFound as e:
                abort(404)

        return jsonify(res)

    @expects_json(schema)
    def post(self):
        data = request.json
        user_service = UserService()
        try:
            user = user_service.save_new(data)

            doctor = self.service.save_new(user, data)
        except (CreateDataFailed, DataExist) as e:
            return {
                "code": "error",
                "msg": str(e)
            }

        return jsonify({
                    'id': doctor.id,
                    'name': doctor.full_name,
                    'gender': doctor.gender,
                    'birthdate': doctor.bod,
                    'work_start_time': doctor.work_start_time.isoformat(),
                    'work_end_time': doctor.work_end_time.isoformat(),
                })

    def put(self, id):
        data = request.json
        try:
            doctor = self.service.get_by_id(id)
            self.service.update(doctor, data)
            return jsonify({
                    'id': doctor.id,
                    'name': doctor.full_name,
                    'gender': doctor.gender,
                    'birthdate': doctor.bod,
                    'work_start_time': doctor.work_start_time.isoformat(),
                    'work_end_time': doctor.work_end_time.isoformat(),
                })
        except DataNotFound as e:
            return {
                "code": "error",
                "msg": f"Data with id: {id} not found !!"
            }

    def delete(self, id):
        self.service.delete(id)
        return {
            "code": "success"
        }


doctor_view = DoctorView.as_view('doctor_view')
app.add_url_rule(
    '/doctors/', view_func=doctor_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/doctors/<int:id>', view_func=doctor_view, methods=['GET', 'PUT', 'DELETE']
)