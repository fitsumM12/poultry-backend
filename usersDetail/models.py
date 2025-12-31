from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class HealthyInstitution(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.name

class usersDetail(AbstractUser):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('BLOCKED', 'Blocked')
    ]
    ROLE_CHOICES = [
        ('SUPER ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User') 
    ]
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    Phone_Number = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    kebele = models.CharField(max_length=100, blank=True, null=True)
    farm = models.CharField(max_length=100, blank=True, null=True)
    farm_institution = models.ForeignKey(HealthyInstitution, on_delete=models.CASCADE, null=True, blank=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=12, blank=True, null=True, choices=STATUS_CHOICES)
    role = models.CharField(max_length=110, blank=True, null=True, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username

