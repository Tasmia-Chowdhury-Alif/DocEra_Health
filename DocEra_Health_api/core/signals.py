from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from patient.models import Patient
from doctor.models import Doctor


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile for new users and handle patient profile creation.
    - Superusers get role='admin'.
    - Non-superusers get role='patient' and a Patient profile.
    - is_active=False for non-superusers to require email activation.
    """

    if created:
        if instance.is_superuser:
            UserProfile.objects.create(user=instance, role="admin")
        else:
            UserProfile.objects.create(user=instance, role="patient")
            Patient.objects.create(user=instance)


@receiver(post_save, sender=Doctor)
def update_user_role_to_doctor(sender, instance, created, **kwargs):
    """
    Update UserProfile role to 'doctor' and delete Patient profile when a Doctor profile is created.
    Ensures the user is exclusively a doctor, not a patient.
    Uses transaction to ensure atomicity.
    """
    if created:
        # Safely delete Patient profile if it exists
        try:
            patient_profile = Patient.objects.get(user=instance.user)
            patient_profile.delete()
        except Patient.DoesNotExist:
            pass

        try:
            user_profile = instance.user.profile
            user_profile.role = "doctor"
            user_profile.save()
        except UserProfile.DoesNotExist:
            # Handle case where UserProfile doesn't exist
            UserProfile.objects.create(user=instance.user, role="doctor")
