from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path ('',views.index,name = 'index'),
    path('users/login', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('upload/',views.upload_sensor_data,name='upload data'),
]
