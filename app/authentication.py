import datetime
from functools import wraps
from flask import request, jsonify
import jwt

from app.main.service.user_service import UserService, User
from app import app

def authenticate(username, password):
    service = UserService()
    user = service.get_filter_data(User.username==username).first()
    print(user)
    if user and user.check_password(password):
        token = jwt.encode({
            'public_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
        },
            app.config['SECRET_KEY'], "HS256")
        return token.decode("utf-8")

def identity(payload):
    service = UserService()
    user_id = payload['identity']
    return service.get_filter_data(User.id==user_id).first()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({'code': 'error', 'msg': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            if datetime.datetime.now().timestamp() > data["exp"]:
                return jsonify({'code': 'error', 'msg': 'token is expired '})

            service = UserService()
            user = service.get_filter_data(User.id == data['public_id']).first()
            current_user = user
        except:
            return jsonify({'code': 'error', 'msg': 'token is invalid'})
        kwargs["current_user"] = current_user
        return f(*args, **kwargs)

    return decorator

