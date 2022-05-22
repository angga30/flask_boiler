import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.exception import DataNotFound, CreateDataFailed, DataExist
from app.main.service.patient_service import PatientService

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



class PatientView(MethodView):
    service = PatientService()
    def get(self, id=None):
        if not id:
            patients = self.service.get_all()
            res = []
            for patient in patients:
                res.append({
                    'id': patient.id,
                    'name': patient.full_name,
                    'gender': patient.gender,
                    'birthdate': patient.bod,
                    'address': patient.address,
                    'no_ktp': patient.no_ktp,
                    'vaccine_type': patient.vaccine_type,
                    'vaccine_count': patient.vaccine_count,
                })
        else:
            try:
                doctor = self.service.get_by_id(id)
                res = {
                    'id': patient.id,
                    'name': patient.full_name,
                    'gender': patient.gender,
                    'birthdate': patient.bod,
                    'address': patient.address,
                    'no_ktp': patient.no_ktp,
                    'vaccine_type': patient.vaccine_type,
                    'vaccine_count': patient.vaccine_count,
                }
            except DataNotFound as e:
                abort(404)

        return jsonify(res)

    @expects_json(schema)
    def post(self):
        data = request.json
        try:
            patient = self.service.save_new(data)
        except (CreateDataFailed, DataExist) as e:
            return {
                "code": "error",
                "msg": str(e)
            }

        return jsonify({
                    'id': patient.id,
                    'name': patient.full_name,
                    'gender': patient.gender,
                    'birthdate': patient.bod,
                    'address': patient.address,
                    'no_ktp': patient.no_ktp,
                    'vaccine_type': patient.vaccine_type,
                    'vaccine_count': patient.vaccine_count,
                })

    def put(self, id):
        data = request.json
        try:
            patient = self.service.get_by_id(id)
            self.service.update(patient, data)
            return jsonify({
                    'id': patient.id,
                    'name': patient.full_name,
                    'gender': patient.gender,
                    'birthdate': patient.bod,
                    'address': patient.address,
                    'no_ktp': patient.no_ktp,
                    'vaccine_type': patient.vaccine_type,
                    'vaccine_count': patient.vaccine_count,
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


patient_view = PatientView.as_view('patient_view')
app.add_url_rule(
    '/patients/', view_func=patient_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/patients/<int:id>', view_func=patient_view, methods=['GET', 'PUT', 'DELETE']
)