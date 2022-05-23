import json, dateparser
from flask import request, jsonify, Blueprint, abort, make_response
from app import db, app
from app.authentication import authenticate

from flask.views import MethodView


class AuthView(MethodView):
    def post(self):
        data = request.json
        if not data or not data["username"] or not data["password"]:
            return make_response('could not verify', 401, {'Authentication': 'login required"'})

        token = authenticate(data["username"], data["password"])
        if token:
            return jsonify({'token': token})

        return make_response('could not verify', 401, {'Authentication': '"login required"'})

auth_view = AuthView.as_view('auth_view')
app.add_url_rule(
    '/login/', view_func=auth_view, methods=['POST']
)