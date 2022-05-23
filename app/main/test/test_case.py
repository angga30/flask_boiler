import re
import unittest
from main import app, db
from app.main.model.user import User
from app.main.model.patient import Patient
from app.main.model.doctor import Doctor

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.populate_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.drop_test_db()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def drop_test_db(self):
        User.query.filter_by(username="susan").delete()
        User.query.filter_by(username="sutoyo").delete()
        User.query.filter_by(username="drhokta").delete()
        Doctor.query.filter_by(full_name="Test Doctor").delete()
        Patient.query.filter_by(no_ktp="52390989899").delete()
        db.session.commit()

    def populate_db(self):
        user = User(full_name="susan nurmantiyo", username='susan', password="12345")
        db.session.add(user)
        db.session.commit()

    def test_login(self):
        resp = self.client.post('login/', json={
            'username': 'susan',
            'password': '12345',
        })
        assert resp.json['token']

    def test_create_patient(self):
        resp = self.client.post('login/', json={
            'username': 'susan',
            'password': '12345',
        })

        resp = self.client.post('patients/',
                                headers={
                                    "Authorization": resp.json['token']
                                },
                                json={
                                    "no_ktp": "52390989899",
                                    "name": "Marlin",
                                    "gender": "L",
                                    "birthdate": "2022-02-12",
                                    "address": "Jl dipati ukur bdg"
                                }
                                )
        assert resp.json["no_ktp"] == "52390989899"
        assert resp.json["name"] == "Marlin"

    def test_create_employee(self):
        resp = self.client.post('login/', json={
            'username': 'susan',
            'password': '12345',
        })

        resp = self.client.post('employees/',
                                headers={
                                    "Authorization": resp.json['token']
                                },
                                json={
                                    "name": "Marlin",
                                    "gender": "L",
                                    "birthdate": "2022-02-12",
                                    "username": "sutoyo",
                                    "password": "lexis"
                                }
                                )
        assert resp.json["name"] == "Marlin"

    def test_create_doctor(self):
        resp = self.client.post('login/', json={
            'username': 'susan',
            'password': '12345',
        })

        resp = self.client.post('doctors/',
                                headers={
                                    "Authorization": resp.json['token']
                                },
                                json={
                                    "name": "Test Doctor",
                                    "gender": "L",
                                    "birthdate": "2022-02-12",
                                    "username": "drhokta",
                                    "password": "lexis",
                                    "work_start_time": "08:11",
                                    "work_end_time": "18:11"
                                }
                                )
        assert resp.json["name"] == "Test Doctor"

if __name__ == '__main__':
    unittest.main()