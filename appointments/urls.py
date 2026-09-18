from django.urls import path
from . import views

urlpatterns = [
    path("availability/", views.doctor_availability, name="doctor_availability"),
    path("book/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("<int:appointment_id>/", views.appointment_details, name="appointment_details"),
    path("success/", views.appointment_success, name="appointment_success"),
]
