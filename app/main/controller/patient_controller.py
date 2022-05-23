import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.authentication import token_required
from app.exception import DataNotFound, CreateDataFailed, DataExist
from app.main.service.patient_service import PatientService

from flask_expects_json import expects_json


schema = {
    "type": "object",
    "properties": {
        "gender": { "type": "string" },
        "name": { "type": "string" },
        "birthdate": { "type": "string" },
        "address": { "type": "string" },
        "no_ktp": { "type": "string" },
      },
    "required": ["gender", "name", "birthdate", "address", "no_ktp"]
}



class PatientView(MethodView):
    service = PatientService()

    @token_required
    def get(self, current_user=None, id=None):
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
                    'appointments': [
                        {
                            'id': appointment.id,
                            'patient': {
                                'id': appointment.patient.id,
                                'name': appointment.patient.full_name,
                                'gender': appointment.patient.gender,
                                'birthdate': appointment.patient.bod,
                                'address': appointment.patient.address,
                                'no_ktp': appointment.patient.no_ktp,
                                'vaccine_type': appointment.patient.vaccine_type,
                                'vaccine_count': appointment.patient.vaccine_count,
                            },
                            'doctor': {
                                'id': appointment.doctor.id,
                                'name': appointment.doctor.full_name,
                            },
                            'status': appointment.status,
                            'diagnose': appointment.diagnose,
                            'notes': appointment.notes,
                        }
                        for appointment in patient.appointments]
                })
        else:
            try:
                patient = self.service.get_by_id(id=id)
                res = {
                    'id': patient.id,
                    'name': patient.full_name,
                    'gender': patient.gender,
                    'birthdate': patient.bod,
                    'address': patient.address,
                    'no_ktp': patient.no_ktp,
                    'vaccine_type': patient.vaccine_type,
                    'vaccine_count': patient.vaccine_count,
                    'appointments': [
                        {
                            'id': appointment.id,
                            'patient': {
                                'id': appointment.patient.id,
                                'name': appointment.patient.full_name,
                                'gender': appointment.patient.gender,
                                'birthdate': appointment.patient.bod,
                                'address': appointment.patient.address,
                                'no_ktp': appointment.patient.no_ktp,
                                'vaccine_type': appointment.patient.vaccine_type,
                                'vaccine_count': appointment.patient.vaccine_count,
                            },
                            'doctor': {
                                'id': appointment.doctor.id,
                                'name': appointment.doctor.full_name,
                            },
                            'status': appointment.status,
                            'diagnose': appointment.diagnose,
                            'notes': appointment.notes,
                        }
                        for appointment in patient.appointments]
                }
            except DataNotFound as e:
                abort(404)

        return jsonify(res)

    @token_required
    @expects_json(schema)
    def post(self, current_user=None):
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

    @token_required
    def put(self, id, current_user=None):
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

    @token_required
    def delete(self, id, current_user=None):
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