from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from doctors.models import Doctor, Hospital
from .models import ConsultationSlot, Appointment


# ============================================================
# DOCTOR AVAILABILITY PAGE
# ============================================================

def doctor_availability(request):

    # Get the active doctor
    doctor = (
        Doctor.objects
        .filter(is_active=True)
        .prefetch_related(
            "hospitals",
            "specialities",
            "treatments"
        )
        .first()
    )

    if not doctor:
        return render(
            request,
            "appointments/availability.html",
            {
                "doctor": None,
                "slots": [],
                "today_slots": [],
                "upcoming_slots": [],
            }
        )

    # Today's date
    today = date.today()

    # Get all available future/current slots
    slots = (
        ConsultationSlot.objects
        .filter(
            doctor=doctor,
            is_available=True,
            date__gte=today
        )
        .select_related("hospital")
        .order_by(
            "date",
            "start_time"
        )
    )

    # Slots available TODAY
    today_slots = slots.filter(
        date=today
    )

    # Upcoming slots
    upcoming_slots = slots.filter(
        date__gt=today
    )

    context = {
        "doctor": doctor,
        "slots": slots,
        "today_slots": today_slots,
        "upcoming_slots": upcoming_slots,
        "today": today,
    }

    return render(
        request,
        "appointments/availability.html",
        context
    )


# ============================================================
# BOOK APPOINTMENT
# ============================================================

@login_required
def book_appointment(request):

    # Get active doctor
    doctor = (
        Doctor.objects
        .filter(is_active=True)
        .prefetch_related("hospitals")
        .first()
    )

    if not doctor:
        messages.error(
            request,
            "Doctor information is currently unavailable."
        )

        return redirect("home")

    # Hospitals associated with this doctor
    hospitals = doctor.hospitals.all()

    # Get only available slots
    slots = (
        ConsultationSlot.objects
        .filter(
            doctor=doctor,
            is_available=True,
            date__gte=date.today()
        )
        .select_related("hospital")
        .order_by(
            "date",
            "start_time"
        )
    )

    # --------------------------------------------------------
    # SLOT SELECTED FROM AVAILABILITY PAGE
    # Example:
    # /appointments/book/?slot=5
    # --------------------------------------------------------

    selected_slot_id = request.GET.get("slot")

    selected_slot = None

    if selected_slot_id:

        try:

            selected_slot = ConsultationSlot.objects.get(
                id=selected_slot_id,
                doctor=doctor,
                is_available=True,
                date__gte=date.today()
            )

        except ConsultationSlot.DoesNotExist:

            messages.error(
                request,
                "The selected appointment slot is not available."
            )

            selected_slot = None

    # --------------------------------------------------------
    # POST - PATIENT SUBMITS APPOINTMENT
    # --------------------------------------------------------

    if request.method == "POST":

        hospital_id = request.POST.get("hospital")
        slot_id = request.POST.get("slot")

        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        reason = request.POST.get("reason")

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not hospital_id:
            messages.error(
                request,
                "Please select a hospital."
            )

            return render(
                request,
                "appointments/book_appointment.html",
                {
                    "doctor": doctor,
                    "hospitals": hospitals,
                    "slots": slots,
                    "selected_slot": selected_slot,
                }
            )

        if not slot_id:
            messages.error(
                request,
                "Please select an available appointment slot."
            )

            return render(
                request,
                "appointments/book_appointment.html",
                {
                    "doctor": doctor,
                    "hospitals": hospitals,
                    "slots": slots,
                    "selected_slot": selected_slot,
                }
            )

        if not phone:
            messages.error(
                request,
                "Please enter your phone number."
            )

            return render(
                request,
                "appointments/book_appointment.html",
                {
                    "doctor": doctor,
                    "hospitals": hospitals,
                    "slots": slots,
                    "selected_slot": selected_slot,
                }
            )

        if not reason:
            messages.error(
                request,
                "Please enter the reason for your appointment."
            )

            return render(
                request,
                "appointments/book_appointment.html",
                {
                    "doctor": doctor,
                    "hospitals": hospitals,
                    "slots": slots,
                    "selected_slot": selected_slot,
                }
            )

        # ----------------------------------------------------
        # GET HOSPITAL
        # ----------------------------------------------------

        try:

            hospital = Hospital.objects.get(
                id=hospital_id,
                doctor__id=doctor.id
            )

        except Hospital.DoesNotExist:

            # Safer fallback because ManyToMany does not support
            # doctor__id on Hospital.objects directly in all setups.

            try:

                hospital = Hospital.objects.get(
                    id=hospital_id
                )

                if not doctor.hospitals.filter(
                    id=hospital.id
                ).exists():

                    raise Hospital.DoesNotExist

            except Hospital.DoesNotExist:

                messages.error(
                    request,
                    "Invalid hospital selected."
                )

                return render(
                    request,
                    "appointments/book_appointment.html",
                    {
                        "doctor": doctor,
                        "hospitals": hospitals,
                        "slots": slots,
                        "selected_slot": selected_slot,
                    }
                )

        # ----------------------------------------------------
        # SAFELY BOOK THE SLOT
        # ----------------------------------------------------

        try:

            with transaction.atomic():

                # Lock the slot while processing the booking.
                # This helps prevent two patients from booking
                # the same slot at the same time.

                slot = (
                    ConsultationSlot.objects
                    .select_for_update()
                    .select_related("hospital", "doctor")
                    .get(
                        id=slot_id,
                        doctor=doctor,
                        hospital=hospital
                    )
                )

                # Check whether slot is still available
                if not slot.is_available:

                    messages.error(
                        request,
                        "Sorry, this appointment slot has already been booked."
                    )

                    return render(
                        request,
                        "appointments/book_appointment.html",
                        {
                            "doctor": doctor,
                            "hospitals": hospitals,
                            "slots": ConsultationSlot.objects.filter(
                                doctor=doctor,
                                is_available=True,
                                date__gte=date.today()
                            ).select_related(
                                "hospital"
                            ).order_by(
                                "date",
                                "start_time"
                            ),
                            "selected_slot": None,
                        }
                    )

                # Check appointment date
                if slot.date < date.today():

                    messages.error(
                        request,
                        "This appointment date has already passed."
                    )

                    return render(
                        request,
                        "appointments/book_appointment.html",
                        {
                            "doctor": doctor,
                            "hospitals": hospitals,
                            "slots": slots,
                            "selected_slot": None,
                        }
                    )

                # ------------------------------------------------
                # CREATE APPOINTMENT
                # ------------------------------------------------

                Appointment.objects.create(

                    patient=request.user,

                    doctor=doctor,

                    hospital=hospital,

                    appointment_date=slot.date,

                    appointment_time=slot.start_time,

                    reason=reason,

                    patient_phone=phone,

                    patient_dob=dob if dob else None,

                    status="Pending"
                )

                # ------------------------------------------------
                # MARK SLOT AS UNAVAILABLE
                # ------------------------------------------------

                slot.is_available = False

                slot.save(
                    update_fields=["is_available"]
                )

            # ----------------------------------------------------
            # SUCCESS
            # ----------------------------------------------------

            return redirect(
                "appointment_success"
            )

        except ConsultationSlot.DoesNotExist:

            messages.error(
                request,
                "The selected appointment slot is no longer available."
            )

    # --------------------------------------------------------
    # PAGE CONTEXT
    # --------------------------------------------------------

    context = {

        "doctor": doctor,

        "hospitals": hospitals,

        "slots": slots,

        "selected_slot": selected_slot,

    }

    return render(
        request,
        "appointments/book_appointment.html",
        context
    )


# ============================================================
# PATIENT MY APPOINTMENTS
# ============================================================

@login_required
def my_appointments(request):
    appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related("doctor", "hospital")
        .order_by("appointment_date", "appointment_time")
    )

    return render(
        request,
        "appointments/my_appointments.html",
        {
            "appointments": appointments,
        }
    )


@login_required
def appointment_details(request, appointment_id):
    appointment = (
        Appointment.objects
        .select_related("doctor", "hospital", "patient")
        .get(id=appointment_id, patient=request.user)
    )

    return render(
        request,
        "appointments/appointment_details.html",
        {
            "appointment": appointment,
        }
    )


# ============================================================
# APPOINTMENT SUCCESS PAGE
# ============================================================

@login_required
def appointment_success(request):

    return render(
        request,
        "appointments/appointment_success.html"
    )