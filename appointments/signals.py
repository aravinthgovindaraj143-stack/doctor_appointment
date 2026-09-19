from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Appointment
from .sms import send_confirmation_sms


@receiver(post_save, sender=Appointment)
def send_appointment_confirmation_sms(sender, instance, **kwargs):
    if instance.status != "Confirmed" or instance.confirmation_sms_sent:
        return

    if send_confirmation_sms(instance):
        sender.objects.filter(pk=instance.pk).update(confirmation_sms_sent=True)