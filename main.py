import os
import unittest, atexit

from flask_migrate import Migrate

from app.main.model import *
from app.main.controller import employee_controller, doctor_controller, patient_controller, appointment_controller, auth_controller

from app import db, app, cron

app.app_context().push()

migrate = Migrate(app, db)

from app.main.jobs import patients_jobs

atexit.register(lambda: cron.shutdown(wait=False))


@app.cli.command()
def start_test():
    tests = unittest.TestLoader().discover('app/main/test')
    result = unittest.TextTestRunner(verbosity=5).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

