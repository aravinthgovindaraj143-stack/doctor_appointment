import logging
import os


logger = logging.getLogger(__name__)


def send_confirmation_sms(appointment):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not all((account_sid, auth_token, from_number)):
        logger.warning(
            "Appointment %s was confirmed, but Twilio SMS settings are missing.",
            appointment.pk,
        )
        return False

    try:
        from twilio.rest import Client

        patient_name = appointment.patient.get_full_name() or appointment.patient.username
        message = (
            f"MedCare: Hello {patient_name}, your appointment with "
            f"{appointment.doctor.full_name} is confirmed for "
            f"{appointment.appointment_date:%d %b %Y} at "
            f"{appointment.appointment_time:%I:%M %p}. "
            f"Hospital: {appointment.hospital.name}."
        )
        Client(account_sid, auth_token).messages.create(
            body=message,
            from_=from_number,
            to=appointment.patient_phone,
        )
    except Exception:
        logger.exception("Could not send confirmation SMS for appointment %s.", appointment.pk)
        return False

    return True