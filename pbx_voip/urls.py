from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ManiDesk.urls')) #incluindo as urls do APP ManiDesk
]
