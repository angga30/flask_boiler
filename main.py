import os
import unittest, atexit

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main.model import *
from app.main.controller import employee_controller
from app.main.controller import doctor_controller

from app import db, app, cron

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

atexit.register(lambda: cron.shutdown(wait=False))

@manager.command
def run():
    app.run()

@manager.command
def test():
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()