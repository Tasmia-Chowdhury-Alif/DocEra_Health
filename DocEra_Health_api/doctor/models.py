from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient

# Create your models here.
STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]


class Designation(models.Model):
    name = models.CharField(max_length= 30)
    slug = models.SlugField(max_length= 40)

    def __str__(self):
        return self.name 
    
class Specialization(models.Model):
    name = models.CharField(max_length= 30)
    slug = models.SlugField(unique=True, max_length= 40)

    def __str__(self):
        return self.name 
    
class AvailableTime(models.Model):
    time = models.CharField(unique=True, max_length= 100)

    def __str__(self):
        return self.time
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    image = models.ImageField(upload_to= "doctor/images/")
    designation = models.ManyToManyField(Designation)
    specialization = models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    fee = models.PositiveIntegerField()
    meet_link = models.CharField(max_length= 200)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete= models.CASCADE, related_name= 'reviews')
    doctor = models.ForeignKey(Doctor, on_delete= models.CASCADE, related_name= 'reviews')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices= STAR_CHOICES, max_length=5)

    def __str__(self):
        return f"Patient: {self.reviewer.user.first_name} ; Doctor: {self.doctor.user.first_name}"

