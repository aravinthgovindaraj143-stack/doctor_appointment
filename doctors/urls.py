from django.urls import path
from . import views

urlpatterns = [
    path('specialties/', views.specialties, name='specialties'),
]
