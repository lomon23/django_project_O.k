from django.contrib import admin
from django.urls import path
  # Імпортуємо views з вашої програми
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
]
