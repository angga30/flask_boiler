import json, dateparser
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.authentication import token_required
from app.exception import DataNotFound, CreateDataFailed, DataExist, ParseError
from app.main.service.appointment_service import AppointmentService, Appointment
from app.main.service.doctor_service import DoctorService, Doctor

from flask_expects_json import expects_json
from sqlalchemy import extract


schema = {
    "type": "object",
    "properties": {
        "patient_id": { "type": "integer" },
        "doctor_id": { "type": "integer" },
        "datetime": { "type": "string" },
        "status": { "type": "string" },
        "diagnose": { "type": "string" },
        "notes": { "type": "string" },
      },
    "required": ["patient_id", "doctor_id", "datetime", "status"]
}



class AppointmentView(MethodView):
    service = AppointmentService()

    @token_required
    def get(self, current_user=None, id=None):
        if not id:
            appointments = self.service.get_all()
            res = []
            for appointment in appointments:
                res.append({
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
                })
        else:
            try:
                appointment = self.service.get_by_id(id=id)
                res = {
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
            except DataNotFound as e:
                abort(404)

        return jsonify(res)

    def _validation_appointment(self, data, is_update=False):
        appointment_time = dateparser.parse(data["datetime"])
        doctor_service = DoctorService()
        doctor = doctor_service.get_filter_data(
            Doctor.id == data["doctor_id"],
            extract('hour', Doctor.work_start_time) <= appointment_time.hour,
            extract('hour', Doctor.work_end_time) >= appointment_time.hour,
        ).first()

        if not doctor:
            raise ParseError("Doctor in those hours is not available !!")

        if not is_update:
            appointment = self.service.get_filter_data(
                extract('month', Appointment.appointment_time) == appointment_time.month,
                extract('year', Appointment.appointment_time) == appointment_time.year,
                extract('day', Appointment.appointment_time) == appointment_time.day,
                extract('hour', Appointment.appointment_time) == appointment_time.hour,
                Appointment.doctor_id == doctor.id
            ).first()

            if appointment:
                raise ParseError("Doctor in those hours is full booked !!")

    @token_required
    @expects_json(schema)
    def post(self, current_user=None):
        data = request.json
        try:
            self._validation_appointment(data)
            appointment = self.service.save_new(data)
        except (CreateDataFailed, DataExist, ParseError) as e:
            return {
                "code": "error",
                "msg": str(e)
            }

        return jsonify({
                    'id': appointment.id,
                    'patient': {
                        'id': appointment.patient.id,
                        'name': appointment.patient.full_name,
                        'gender': appointment.patient.gender,
                        'birthdate': appointment.patient.bod.isoformat(),
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
                })

    @token_required
    @expects_json(schema)
    def put(self, id, current_user=None):
        data = request.json
        try:
            self._validation_appointment(data, True)
            appointment = self.service.get_by_id(id=id)
            self.service.update(appointment, data)
            return jsonify(
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
            )
        except (CreateDataFailed,DataNotFound, ParseError) as e:
            return {
                "code": "error",
                "msg": str(e)
            }

    @token_required
    def delete(self, id, current_user):
        self.service.delete(id)
        return {
            "code": "success"
        }


appointment_view = AppointmentView.as_view('appointment_view')
app.add_url_rule(
    '/appointments/', view_func=appointment_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/appointments/<int:id>', view_func=appointment_view, methods=['GET', 'PUT', 'DELETE']
)