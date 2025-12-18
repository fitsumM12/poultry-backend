from django.urls import path
from .views import *

urlpatterns = [
    path('users/', fetch_users_api, name='fetch_users'),
    path('users/<int:pk>/', fetch_user_api, name='fetch_user'),
    path('users/update/<int:pk>/', update_user_api, name='update_user'),
    path('users/approve/<int:pk>/', approve_user_api, name='approve_user'),
    path('users/block/<int:pk>/', block_user_api, name='block_user'),
    path('users/delete/<int:pk>/', delete_user_api, name='delete_user'),
    path('users/add/', add_user_api, name='add_user'),
    path('users/upload_files/', upload_files, name='upload_files'),
    path('users/login/', login, name='login'),
    path('users/refresh-token/', refresh_token, name='refresh_token'),
    path('institute/get_healthy_institution_count', get_healthy_institution_count, name='get_healthy_institution_count')
]
