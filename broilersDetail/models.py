from django.db import models
from usersDetail.models import usersDetail, HealthyInstitution
from django.utils import timezone

class broilersDetail(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    farmer_name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=100)
    hatch_date = models.DateField(null=True, blank=True)
    breed = models.CharField(max_length=110, blank=True)
    Flock_ID = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    Phone_Number = models.CharField(max_length=20,blank=True, null=True)
    record_date = models.DateField(default=timezone.now)
    region = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=100, blank=True)
    kebele = models.CharField(max_length=100, blank=True)
    supervisor_id = models.ForeignKey(usersDetail, on_delete=models.CASCADE, null=True, blank=True)
    farm_institution = models.ForeignKey(HealthyInstitution, on_delete=models.CASCADE, null=True,
    blank=True)
  
    def __str__(self):
        return f"{self.farmer_name} {self.farm_name}"


class broilersImageAndPrediction(models.Model):    
    id = models.AutoField(primary_key=True, unique=True)
    image_url = models.CharField(max_length=200, blank=True)
    health_status = models.CharField(max_length=200, blank=True)
    record_date = models.DateField(default=timezone.now)
    broiler_id = models.ForeignKey(broilersDetail, on_delete=models.CASCADE)  
    supervisor_id = models.ForeignKey(usersDetail, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.broiler_id_id)


class PhysicianDecision(models.Model):
    result = models.ForeignKey(broilersImageAndPrediction, on_delete=models.CASCADE, unique=False)
    approval = models.BooleanField(default=True,null=True)
    feedback = models.TextField(blank=True)
    disease = models.TextField(max_length=200, null=True, default="")
    created = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.created)    