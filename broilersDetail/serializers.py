from rest_framework import serializers
# from urllib3 import request
from .models import *

from django.utils import timezone
class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = usersDetail
        fields = "__all__"

class BroilersDetailSerializer(serializers.ModelSerializer):

    farm_name = serializers.CharField(write_only=True, required=False)

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
        read_only_fields = ['record_date']


    # ✅ MUST BE INSIDE CLASS
    def create(self, validated_data):
        from .models import Farm

        request = self.context.get('request')
        user = request.user

        farm_name = validated_data.pop('farm_name', None)

        # institution = getattr(user, 'farm_institution', None)

        if not user.farm:
            raise serializers.ValidationError(
                "User has no institution assigned."
            )
        institution = user.farm.institution



        farm_obj = None
        if farm_name:
            farm_obj, _ = Farm.objects.get_or_create(
                name=farm_name,
                institution=institution
            )

        validated_data['farm'] = farm_obj
        validated_data['supervisor'] = user

        return broilersDetail.objects.create(**validated_data)
class BroilersImageAndPredictionSerializer(serializers.ModelSerializer):
    # 1. Map the DB field 'image_url' to the name 'broiler_image' for React
    # broiler_image = serializers.CharField(source='image_url', read_only=True)
    broiler_image = serializers.SerializerMethodField()
    
    # 2. Map the DB field 'health_status' to 'image_prediction' for React
    image_prediction = serializers.CharField(source='health_status', read_only=True)
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
    # YOU MUST ADD THIS FUNCTION
    def get_broiler_image(self, obj):
        if obj.broiler_image:
            # This points to the /media/raw/ folder seen in your file structure
            return f"/media/raw/{obj.broiler_image}"
        return None
    def create(self, validated_data):
        # Ensure health_status is set to Pending if not provided
        if 'health_status' not in validated_data:
            validated_data['health_status'] = "Pending..."
        return super().create(validated_data)
    

class PhysicianDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicianDecision
        fields = ['approval', 'feedback', 'disease', 'result'] 
    def create(self, validated_data):
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
