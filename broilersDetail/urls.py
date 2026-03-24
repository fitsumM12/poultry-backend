from django.urls import path
from . import views
from .views import add_image_predictions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# urlpatterns = [
#     path("token/", TokenObtainPairView.as_view()),
#     path("token/refresh/", TokenRefreshView.as_view()),
# #  # Redirect /add_image_predictions/ to the same view
#     # path('broilers/add_image_predictions/', views.upload_raw_generate_cam_and_predictions, name='add_image_predictions'),
# #    path('broilers/', views.fetch_broilers_api, name='fetch_broilers_api'),
# #     path('broilers/<int:pk>/', views.fetch_broiler_api, name='fetch_broiler_api'),
# #     path('broilers/add/', views.add_broiler_api, name='add_broiler_api'),
# #     path('broilers/update/<int:pk>/', views.update_broiler_api, name='update_broiler_api'),
# #     path('broilers/delete/<int:pk>/', views.delete_broiler_api, name='delete_broiler_api'),
#       path('broilers/predict_image/', views.upload_raw_generate_cam_and_predictions, name='upload_raw_generate_cam_and_predictions'),
# #     path('broilers/supervisor/<int:pk>/', views.fetch_broilers_supervisor_api, name ='fetch_broilers_supervisor_api'),
# #     path('broilers/add_health_status/', views.broilersImageAndPrediction, name='update_broiler_api'),
# #     # path('broilers/add_health_status/', views.add_broilers_image_and_prediction, name='update_broiler_api'),
# #     # path('broilers/getprediction/<int:id>/', views.get_broiler_by_id, name="get_predictions"),
# #     # path('getprediction/<int:id>/', views.get_broiler_by_id, name="get_predictions"),
# #     path('getprediction/<int:id>/',views.get_broiler_latest_prediction,name="get_latest_prediction"),
# #     path('broilers/add_image_predictions/', views.add_broilers_image_and_prediction, name='add_image_predictions'),
# #     path('broilers/addphysiciandecision/', views.add_physician_decision, name ="add_physician_decision"),
#     path('broilers/count_broilers_json/', views.count_broilers_json, name="count_broilers_json"),
#     path('broilers/breed_count/', views.breed_count, name="breed_count"),
# #     path('broilers/broiler_registration_trends/', views.broiler_registration_trends, name="broiler_registration_trends"),
# #     path('broilers/predictive_outcomes_trends/', views.predictive_outcomes_trends, name="predictive_outcomes_trends"),
# #     path('broilers/breed_distribution_trends/', views.breed_distribution_trends, name="breed_distribution_trends"),
#     path('broilers/monthly_broiler_count/<int:year>/', views.monthly_broiler_count, name='monthly-broiler-count'),
# #     path('broilers/predictions_by_month/<int:year>/', views.predictions_by_month, name='predictions-by-month'),
# #     path('broilers/broiler_count_per_institution/', views.broiler_count_per_institution, name='broiler_count_per_institution'),
# #     path('broilers/new_vs_returning_broilers/', views.new_vs_returning_broilers, name='new_vs_returning_broilers'),
    
# # ]
#  # BROILER CRUD
#     # -------------------------
#     path('broilers/', views.fetch_broilers_api, name='fetch_broilers'),
#     path('broilers/<int:pk>/', views.fetch_broiler_api, name='fetch_broiler'),
#     path('broilers/add/', views.add_broiler_api, name='add_broiler'),
#     path('broilers/update/<int:pk>/', views.update_broiler_api, name='update_broiler'),
#     path('broilers/delete/<int:pk>/', views.delete_broiler_api, name='delete_broiler'),
#     path('broilers/supervisor/<int:pk>/', views.fetch_broilers_supervisor_api, name='fetch_broilers_supervisor'),

#     # -------------------------
#     # IMAGE + PREDICTION
#     # -------------------------
#     path('broilers/upload_image/', views.upload_raw_generate_cam_and_predictions, name='upload_image_and_predict'),

#     # -------------------------
#     # COUNTS & STATS
#     # -------------------------
#     path('broilers/breed_count/', views.breed_count, name='breed_count'),
#     path('broilers/registration_trends/', views.broiler_registration_trends, name='registration_trends'),
#     path('broilers/count_per_institution/', views.broiler_count_per_institution, name='broiler_count_per_institution'),
#     # path('predict_image/',views.upload_raw_generate_cam_and_predictions,name='predict_image'),
#     path('broilers/add_image_predictions/', add_image_predictions, name='add_image_predictions'),]
urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    # BROILER CRUD
    path('broilers/', views.fetch_broilers_api, name='fetch_broilers'),
    path('broilers/<int:pk>/', views.fetch_broiler_api, name='fetch_broiler'),
    path('broilers/add/', views.add_broiler_api, name='add_broiler'),
    path('broilers/update/<int:pk>/', views.update_broiler_api, name='update_broiler'),
    path('broilers/delete/<int:pk>/', views.delete_broiler_api, name='delete_broiler'),
    path('broilers/supervisor/<int:pk>/', views.fetch_broilers_supervisor_api, name='fetch_broilers_supervisor'),

    # IMAGE
    path('broilers/upload_image/', views.upload_raw_generate_cam_and_predictions, name='upload_image_and_predict'),

    # STATS
    path('broilers/breed_count/', views.breed_count, name='breed_count'),
    path('broilers/registration_trends/', views.broiler_registration_trends, name='registration_trends'),
    path('broilers/count_per_institution/', views.broiler_count_per_institution, name='broiler_count_per_institution'),

    # ✅ ADD THESE (IMPORTANT)
    path('broilers/count_broilers_json/', views.count_broilers_json, name="count_broilers_json"),
    path('broilers/monthly_broiler_count/<int:year>/', views.monthly_broiler_count, name='monthly-broiler-count'),

    # IMAGE PREDICTIONS
    path('broilers/add_image_predictions/', add_image_predictions, name='add_image_predictions'),
    path('broilers/predict_image/', views.upload_raw_generate_cam_and_predictions),
    path('broilers/farm/<int:pk>/', views.fetch_broilers_supervisor_api),
    path('broilers/getprediction/<int:broiler_id>/', views.get_latest_prediction, name='get_latest_prediction'),
]