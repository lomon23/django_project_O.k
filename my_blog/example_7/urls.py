from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Адмінка
    path('', views.main_page, name='home'),  # Головна сторінка
]
