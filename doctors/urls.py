from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctors_list, name='doctors_list'),
    path('treatments/', views.treatments, name='treatments'),
    path('specialties/', views.specialties, name='specialties'),
]
