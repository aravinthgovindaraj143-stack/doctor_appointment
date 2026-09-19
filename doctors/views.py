from django.shortcuts import render
from .models import Doctor


def specialties(request):
	doctor = Doctor.objects.filter(is_active=True).prefetch_related(
		"specialities"
	).first()

	return render(
		request,
		"doctors/specialties.html",
		{
			"doctor": doctor,
			"specialties": doctor.specialities.all() if doctor else [],
		},
	)
