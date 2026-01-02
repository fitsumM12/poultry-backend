from django.urls import path
from . import views

urlpatterns = [
    path('broilers/', views.fetch_broilers_api, name='fetch_broilers_api'),
    path('broilers/<int:pk>/', views.fetch_broiler_api, name='fetch_broiler_api'),
    path('broilers/add/', views.add_broiler_api, name='add_broiler_api'),
    path('broilers/update/<int:pk>/', views.update_broiler_api, name='update_broiler_api'),
    path('broilers/delete/<int:pk>/', views.delete_broiler_api, name='delete_broiler_api'),
    path('broilers/predict_image/', views.upload_raw_generate_cam_and_predictions, name='upload_raw_generate_cam_and_predictions'),
    path('broilers/supervisor/<int:pk>/', views.fetch_broilers_supervisor_api, name ='fetch_broilers_supervisor_api'),
    path('broilers/add_health_status/', views.add_broilers_image_and_prediction, name='update_broiler_api'),
    # path('broilers/getprediction/<int:id>/', views.get_broiler_by_id, name="get_predictions"),
    path('getprediction/<int:id>/', views.get_broiler_by_id, name="get_predictions"),
    path('broilers/add_image_predictions/', views.add_broilers_image_and_prediction, name='add_image_predictions'),

    path('broilers/addphysiciandecision/', views.add_physician_decision, name ="add_physician_decision"),
    path('broilers/count_broilers_json/', views.count_broilers_json, name="count_broilers_json"),
    path('broilers/breed_count/', views.breed_count, name="breed_count"),
    path('broilers/broiler_registration_trends/', views.broiler_registration_trends, name="broiler_registration_trends"),
    path('broilers/predictive_outcomes_trends/', views.predictive_outcomes_trends, name="predictive_outcomes_trends"),
    path('broilers/breed_distribution_trends/', views.breed_distribution_trends, name="breed_distribution_trends"),
    path('broilers/monthly_broiler_count/<int:year>/', views.monthly_broiler_count, name='monthly-broiler-count'),
    path('broilers/predictions_by_month/<int:year>/', views.predictions_by_month, name='predictions-by-month'),
    path('broilers/broiler_count_per_institution/', views.broiler_count_per_institution, name='broiler_count_per_institution'),
    path('broilers/new_vs_returning_broilers/', views.new_vs_returning_broilers, name='new_vs_returning_broilers'),
    
]