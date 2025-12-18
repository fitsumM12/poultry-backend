from django.db import models
from usersDetail.models import usersDetail, HealthyInstitution
from django.utils import timezone

class patientsDetail(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=110)
    job = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    record_date = models.DateField(default=timezone.now)
    region = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=100, blank=True)
    kebele = models.CharField(max_length=100, blank=True)
    doctor_id = models.ForeignKey(usersDetail, on_delete=models.CASCADE)
    health_institution = models.ForeignKey(HealthyInstitution, on_delete=models.CASCADE)
  
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class patientsImageAndPrediction(models.Model):    
    id = models.AutoField(primary_key=True, unique=True)
    image_url = models.CharField(max_length=200, blank=True)
    image_prediction = models.CharField(max_length=200, blank=True)
    record_date = models.DateField(default=timezone.now)
    patient_id = models.ForeignKey(patientsDetail, on_delete=models.CASCADE)  
    doctor_id= models.ForeignKey(usersDetail, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.patient_id)


class PhysicianDecision(models.Model):
    result = models.ForeignKey(patientsImageAndPrediction, on_delete=models.CASCADE, unique=False)
    approval = models.BooleanField(default=True,null=True)
    feedback = models.TextField(blank=True)
    disease = models.TextField(max_length=200, null=True, default="")
    created = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.created)    