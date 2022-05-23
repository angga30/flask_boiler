#
# from google.cloud import bigquery
# from app.exception import DataExist, DataNotFound
# from app.main.service.patient_service import PatientService
# from app import cron, app
#
#
# def process_patient_update():
#     with app.app_context():
#         client = bigquery.Client()
#         service = PatientService()
#
#         patient_data = client.query("""
#         select * from `delman-interview.interview_mock_data.vaccine-data`
#         """)
#
#         for patient_vaction in patient_data:
#             try:
#                 patient = service.get_by_id(no_ktp=str(patient_vaction[0]))
#                 patient.vaccine_type = patient_vaction[1]
#                 patient.vaccine_count = patient_vaction[2]
#                 service.update(patient)
#             except DataNotFound as e:
#                 print(e)
#                 continue
#
#
# cron.add_job(process_patient_update, 'cron',  minute='02', hour='04')
