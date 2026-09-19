from django.contrib import admin
from .models import Appointment, ConsultationSlot


@admin.register(ConsultationSlot)
class ConsultationSlotAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "hospital",
        "date",
        "start_time",
        "end_time",
        "is_available",
    )

    list_filter = (
        "date",
        "is_available",
        "doctor",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "hospital",
        "appointment_date",
        "appointment_time",
        "status",
        "confirmation_sms_sent",
    )

    list_filter = (
        "status",
        "appointment_date",
        "doctor",
    )

    search_fields = (
        "patient__username",
        "doctor__full_name",
        "patient_phone",
    )