from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.fetch_patients_api, name='fetch_patients_api'),
    path('patients/<int:pk>/', views.fetch_patient_api, name='fetch_patient_api'),
    path('patients/add/', views.add_patient_api, name='add_patient_api'),
    path('patients/update/<int:pk>/', views.update_patient_api, name='update_patient_api'),
    path('patients/delete/<int:pk>/', views.delete_patient_api, name='delete_patient_api'),
    path('patients/predict_image/', views.upload_raw_generate_cam_and_predictions, name='upload_raw_generate_cam_and_predictions'),
    path('patients/doctor/<int:pk>/', views.fetch_patients_doctor_api, name ='fetch_patients_doctor_api'),
    path('patients/add_image_predictions/', views.add_patients_image_and_prediction, name='update_patient_api'),
    path('patients/getprediction/<int:id>/', views.get_patient_by_id, name="get_predictions"),
    path('patients/addphysiciandecision/', views.add_physician_decision, name ="add_physician_decision"),
    path('patients/count_patients_json/', views.count_patients_json, name="count_patients_json"),
    path('patients/gender_count/', views.gender_count, name="gender_count"),
    path('patients/patient_registration_trends/', views.patient_registration_trends, name="patient_registration_trends"),
    path('patients/predictive_outcomes_trends/', views.predictive_outcomes_trends, name="predictive_outcomes_trends"),
    path('patients/gender_distribution_trends/', views.gender_distribution_trends, name="gender_distribution_trends"),
    path('patients/monthly_patient_count/<int:year>/', views.monthly_patient_count, name='monthly-patient-count'),
    path('patients/predictions_by_month/<int:year>/', views.predictions_by_month, name='predictions-by-month'),
    path('patients/patient_count_per_institution/', views.patient_count_per_institution, name='patient_count_per_institution'),
    path('patients/new_vs_returning_patients/', views.new_vs_returning_patients, name='new_vs_returning_patients'),
    
]