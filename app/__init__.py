from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os

from .config import config_state_name
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_state_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

cron = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
cron.start()