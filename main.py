import os
import unittest, atexit

from flask_migrate import Migrate

from app.main.model import *
from app.main.controller import employee_controller
from app.main.controller import doctor_controller

from app import db, app, cron

app.app_context().push()

migrate = Migrate(app, db)

atexit.register(lambda: cron.shutdown(wait=False))

