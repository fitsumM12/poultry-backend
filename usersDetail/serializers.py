# from rest_framework import serializers
# from .models import usersDetail, HealthyInstitution

# class HealthyInstitutionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HealthyInstitution
#         fields = ['id', 'name', 'created'] 


# class UserDetailSerializer(serializers.ModelSerializer):
#     farm_institution = HealthyInstitutionSerializer() 
#     farmer_name = serializers.SerializerMethodField()
#     farm_name = serializers.SerializerMethodField()

#     class Meta:
#         model = usersDetail
#         fields = [
#             'id', 'farmer_name', 'farm_name','birthday',  'email', 'Phone_Number', 'region', 'zone', 'kebele',
#             'farm', 'farm_institution', 'image', 'passport', 'status', 'role'
#         ]
#     # Make sure the method names match exactly
#     def get_farmer_name(self, obj):
#         # obj is a usersDetail instance
#         return obj.get_full_name()  # first_name + last_name

#     def get_farm_name(self, obj):
#         return obj.farm  # your farm field
from rest_framework import serializers
from .models import usersDetail, HealthyInstitution


class HealthyInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthyInstitution
        fields = ['id', 'name', 'created']


class UserDetailSerializer(serializers.ModelSerializer):
    farm_institution = serializers.SerializerMethodField()
    farmer_name = serializers.SerializerMethodField()
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = usersDetail
        fields = [
            'id',
            'farmer_name',
            'farm_name',
            'birthday',
            'email',
            'Phone_Number',
            'region',
            'zone',
            'kebele',
            'farm',
            'farm_institution',
            'image',
            'passport',
            'status',
            'role'
        ]

    def get_farmer_name(self, obj):
        return obj.get_full_name()

    def get_farm_name(self, obj):
        return obj.farm.name if obj.farm else None

    def get_farm_institution(self, obj):
        if obj.farm:
            return HealthyInstitutionSerializer(obj.farm.institution).data
        return None