from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os

from .config import config_state_name
from apscheduler.scheduler import Scheduler

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

cron = Scheduler(daemon=True)
cron.start()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_state_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')