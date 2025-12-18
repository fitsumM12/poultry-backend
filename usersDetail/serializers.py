from rest_framework import serializers
from .models import usersDetail, HealthyInstitution

class HealthyInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthyInstitution
        fields = ['id', 'name', 'created'] 


class UserDetailSerializer(serializers.ModelSerializer):
    health_institution = HealthyInstitutionSerializer() 

    class Meta:
        model = usersDetail
        fields = [
            'id', 'first_name', 'last_name','birthday', 'gender', 'email', 'mobile', 'region', 'zone', 'kebele',
            'hospital', 'health_institution', 'image', 'passport', 'status', 'role'
        ]