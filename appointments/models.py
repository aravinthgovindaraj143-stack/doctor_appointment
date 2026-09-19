from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor, Hospital


class ConsultationSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="consultation_slots"
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.doctor.full_name} - "
            f"{self.date} - "
            f"{self.start_time}"
        )


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    patient_phone = models.CharField(max_length=20)
    patient_dob = models.DateField(
        blank=True,
        null=True
    )

    admin_notes = models.TextField(blank=True)

    confirmation_sms_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.patient.username} - "
            f"{self.doctor.full_name} - "
            f"{self.appointment_date}"
        )
