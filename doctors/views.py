from django.shortcuts import render
from .models import Doctor


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
