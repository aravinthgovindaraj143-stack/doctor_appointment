from django.shortcuts import render
from .models import Doctor, Treatment


def doctors_list(request):
	doctors = Doctor.objects.filter(
		is_active=True
	).prefetch_related(
		"specialities",
		"treatments",
		"hospitals",
	).order_by("created_at", "full_name")

	return render(
		request,
		"doctors/doctors_list.html",
		{"doctors": doctors},
	)


def treatments(request):
	treatments = Treatment.objects.prefetch_related(
		"doctor_set",
	).order_by("name")

	return render(
		request,
		"doctors/treatments.html",
		{"treatments": treatments},
	)


def specialties(request):
	doctors = Doctor.objects.filter(is_active=True).prefetch_related(
		"specialities"
	).order_by("created_at")
	doctor = doctors.first()

	return render(
		request,
		"doctors/specialties.html",
		{
			"doctor": doctor,
			"doctors": doctors,
			"specialties": doctor.specialities.all() if doctor else [],
		},
	)
