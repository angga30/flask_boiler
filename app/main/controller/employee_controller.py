import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.authentication import token_required
from app.exception import DataNotFound, CreateDataFailed, DataExist
from app.main.service.employee_service import EmployeeService
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
      },
    "required": ["username", "password", "birthdate"]
}



class EmployeeView(MethodView):
    service = EmployeeService()

    @token_required
    def get(self, current_user=None, id=None):
        if not id:
            employees = self.service.get_all()
            res = []
            for employee in employees:
                res.append({
                    'id': employee.id,
                    'name': employee.full_name,
                    'gender': employee.gender,
                    'birthdate': employee.bod,
                })
        else:
            try:
                employee = self.service.get_by_id(id)
                res = {
                    'id': employee.id,
                    'name': employee.full_name,
                    'gender': employee.gender,
                    'birthdate': employee.bod,
                }
            except DataNotFound as e:
                abort(404)

        return jsonify(res)

    @token_required
    @expects_json(schema)
    def post(self, current_user=None):
        data = request.json
        user_service = UserService()
        try:
            user = user_service.save_new(data)

            employee = self.service.save_new(user, data)
        except (CreateDataFailed, DataExist) as e:
            return {
                "code": "error",
                "msg": str(e)
            }

        return jsonify({
            "id": employee.id,
            "name": employee.full_name,
            "birthdate": employee.bod,
            "gender": employee.gender
        })

    @token_required
    def put(self, id, current_user=None):
        data = request.json
        try:
            employee = self.service.get_by_id(id)
            self.service.update(employee, data)
            return jsonify({
                "id": employee.id,
                "name": employee.full_name,
                "birthdate": employee.bod,
                "gender": employee.gender
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


employee_view = EmployeeView.as_view('employee_view')
app.add_url_rule(
    '/employees/', view_func=employee_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/employees/<int:id>', view_func=employee_view, methods=['GET', 'PUT', 'DELETE']
)