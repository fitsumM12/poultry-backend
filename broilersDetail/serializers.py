from rest_framework import serializers
from .models import *

from django.utils import timezone
class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = usersDetail
        fields = "__all__"
class FarmInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthyInstitution
        fields = "__all__"
class BroilersDetailSerializer(serializers.ModelSerializer):
    farm_institution = FarmInstitutionSerializer(read_only=True)
    # supervisor_id = UsersDetailSerializer(read_only=True)
    supervisor = UsersDetailSerializer(read_only=True)
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=usersDetail.objects.all(), 
        source='supervisor', 
        write_only=True, 
        required=False,
        allow_null=True
    )

    class Meta:
        model = broilersDetail
        fields = '__all__'
        

    def create(self, validated_data):
        validated_data['record_date'] = timezone.now().date() 
        # validated_data['breed'] = "Female"
        return super().create(validated_data)

class BroilersImageAndPredictionSerializer(serializers.ModelSerializer):
    # This maps the "supervisor_id" key from React to the "supervisor" field in the DB
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=usersDetail.objects.all(), 
        source='supervisor', 
        write_only=True, 
        required=False
    )
    class Meta:
        model = broilersImageAndPrediction
        fields = '__all__'
    def create(self, validated_data):
        validated_data['record_date'] = timezone.now().date() 
        return super().create(validated_data)
    

class PhysicianDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicianDecision
        fields = ['approval', 'feedback', 'disease', 'result'] 
    def create(self, validated_data):
        validated_data['created'] = timezone.now().date() 
        return super().create(validated_data)

class MonthlyBroilerCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    broiler_count = serializers.IntegerField()


class MonthlyPredictionSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=3) 
    prediction_count = serializers.IntegerField()

class MonthlyFollowUpSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=3)
    followup_count = serializers.IntegerField()
