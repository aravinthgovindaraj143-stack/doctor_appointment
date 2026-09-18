from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    full_name = models.CharField(max_length=200)
    profile_image = models.ImageField(
        upload_to="doctors/",
        blank=True,
        null=True
    )

    designation = models.CharField(max_length=200)
    qualifications = models.TextField()
    registration_number = models.CharField(
        max_length=100,
        blank=True
    )

    biography = models.TextField()
    experience = models.PositiveIntegerField(
        help_text="Experience in years"
    )

    specialities = models.ManyToManyField(
        Speciality,
        blank=True
    )

    treatments = models.ManyToManyField(
        Treatment,
        blank=True
    )

    hospitals = models.ManyToManyField(
        Hospital,
        blank=True
    )

    consultation_information = models.TextField(
        blank=True
    )

    research = models.TextField(blank=True)
    memberships = models.TextField(blank=True)
    languages = models.CharField(
        max_length=300,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name