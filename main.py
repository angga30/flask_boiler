import os
import unittest, atexit

from flask_migrate import Migrate

from app.main.model import *
from app.main.controller import employee_controller, doctor_controller, patient_controller

from app import db, app, cron

app.app_context().push()

migrate = Migrate(app, db)

from app.main.jobs import patients_jobs

atexit.register(lambda: cron.shutdown(wait=False))

