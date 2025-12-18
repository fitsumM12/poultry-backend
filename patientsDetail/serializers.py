from rest_framework import serializers
from .models import *

from django.utils import timezone

class PatientsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = patientsDetail
        fields = '__all__'

    def create(self, validated_data):
        validated_data['record_date'] = timezone.now().date() 
        validated_data['gender'] = "Female"
        return super().create(validated_data)

class patientsImageAndPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = patientsImageAndPrediction
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

class MonthlyPatientCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    patient_count = serializers.IntegerField()


class MonthlyPredictionSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=3) 
    prediction_count = serializers.IntegerField()

class MonthlyFollowUpSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=3)
    followup_count = serializers.IntegerField()
