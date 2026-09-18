from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from appointments.models import Appointment


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def profile_view(request):
    appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related("doctor", "hospital")
        .order_by("appointment_date", "appointment_time")
    )

    upcoming = appointments.filter(status__in=["Pending", "Confirmed"]).order_by("appointment_date", "appointment_time")
    next_visit = upcoming.first()

    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user,
            "appointments": appointments,
            "upcoming": upcoming,
            "next_visit": next_visit,
            "appointment_count": appointments.count(),
        },
    )