from django.db import models
from patient.models import Patient
from doctor.models import Doctor, AvailableTime

# Create your models here.
APPOINTMENT_TYPE = [
    ("Offline", "Offline"),
    ("Online", "Online"),
]
APPOINTMENT_STATUS = [
    ("Pending", "Pending"),
    ("Running", "Running"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]
PAYMENT_STATUS = [
    ("unpaid", "Unpaid"),
    ("paid", "Paid"),
    ("failed", "Failed"),
    ("refunded", "Refunded"),
]


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    appointment_type = models.CharField(choices=APPOINTMENT_TYPE, max_length=10)
    appointment_status = models.CharField(choices=APPOINTMENT_STATUS, max_length=10, default="Pending")
    payment_status = models.CharField(choices=PAYMENT_STATUS, default="unpaid", verbose_name="Payment Status")
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    symptom = models.TextField(max_length=500)
    time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Doctor: {self.doctor.user.first_name} , Patient: {self.patient.user.first_name}"

    class Meta:
        ordering = ["-created_at"]
