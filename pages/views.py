from django.shortcuts import render, redirect
from django.contrib import messages
from doctors.models import Doctor, Speciality
from .models import ContactMessage


def home(request):
    doctors = Doctor.objects.filter(
        is_active=True
    ).prefetch_related(
        "specialities",
        "treatments",
        "hospitals"
    ).order_by("created_at")

    doctor = doctors.first()
    specialties = Speciality.objects.all().order_by("name")

    return render(
        request,
        "pages/home.html",
        {
            "doctor": doctor,
            "doctors": doctors,
            "specialties": specialties,
        }
    )


def about(request):
    doctors = Doctor.objects.filter(
        is_active=True
    ).prefetch_related(
        "specialities",
        "treatments",
        "hospitals"
    ).order_by("created_at")
    doctor = doctors.first()

    return render(
        request,
        "pages/about.html",
        {
            "doctor": doctor,
            "doctors": doctors,
        }
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not all([name, email, message]):
            messages.error(request, "Please fill in your name, email, and message.")
        else:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
            )
            messages.success(request, "Thank you. Your message has been sent successfully.")
            return redirect("contact")

    return render(request, "pages/contact.html")