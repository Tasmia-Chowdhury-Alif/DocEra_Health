from django.contrib import admin
from .models import Appointment

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor_name', 'patient_name', 'appointment_type', 'appointment_status', 'symptom', 'time', 'cancel']

    def doctor_name(self, obj):
        return obj.doctor.user.first_name

    def patient_name(self, obj):
        return obj.patient.user.first_name
    
    def save_model(self, request, obj, form, change):
        if obj.appointment_type == "Online" and obj.appointment_status == "Running" :
            email_subject = "Yor Online Appointment is Running"
            email_body = render_to_string('./appointment/appointment_email.html', {"user" : obj.patient.user, "doctor" : obj.doctor})

            email = EmailMultiAlternatives(email_subject, '', to=[obj.patient.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
        return super().save_model(request, obj, form, change)
    
admin.site.register(Appointment, AppointmentAdmin)