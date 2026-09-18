from django.contrib import admin
from .models import Doctor, Hospital, Speciality, Treatment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'designation',
        'experience',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'experience')
    search_fields = (
        'full_name',
        'designation',
        'registration_number',
        'qualifications',
    )
    filter_horizontal = ('specialities', 'treatments', 'hospitals')
    readonly_fields = ('created_at',)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')
    search_fields = ('name', 'city', 'address')


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')