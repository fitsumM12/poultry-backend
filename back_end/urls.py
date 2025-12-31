from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# In your app's urls.py
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Broiler Disease Detection App!")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('usersDetail.urls')),
    path('api/', include('broilersDetail.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)