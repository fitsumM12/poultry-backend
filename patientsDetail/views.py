from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import patientsDetail
from django.http import JsonResponse
from .serializers import *
from .predictor import *
from django.db.models import Q
from tensorflow.keras.preprocessing import image
import os
import cv2
from django.conf import settings
from PIL import Image
import numpy as np
from .predictor import create_model, load_weights
from django.contrib.auth.decorators import login_required
from .preprocess import circle_crop
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import patientsDetail
import tensorflow as tf

@api_view(['GET'])
@permission_classes([])
def fetch_patients_api(request):
    patients = patientsDetail.objects.all()
    serializer = PatientsDetailSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_patients_doctor_api(request, pk):
    patients = patientsDetail.objects.filter(health_institution=pk)
    serializer = PatientsDetailSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def fetch_patient_api(request, pk):
    patient = patientsDetail.objects.get(pk=pk)
    serializer = PatientsDetailSerializer(patient)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_patient_api(request, pk):
    patient = patientsDetail.objects.get(pk=pk)
    serializer = PatientsDetailSerializer(patient, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_patient_api(request, pk):
    patient = patientsDetail.objects.get(pk=pk)
    patient.delete()
    return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient_api(request):
    serializer = PatientsDetailSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        response_data = {
            'id': patient.id,
            **serializer.data
        }
        return Response(response_data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_raw_generate_cam_and_predictions(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file found'}, status=400)

    image_file = request.FILES.get('image')
    image_name = image_file.name  
    image_path = os.path.join(settings.MEDIA_ROOT_RAW, image_name)
    
    with open(image_path, 'wb') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # image = Image.open(image_path)
    # image = image.resize((512, 512))
    # image = np.array(image) / 255.0
    img = image.load_img(image_path, target_size=(512, 512, 3))  
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)
    img_array = datagen.standardize(img_array)  # Rescale the image


    # predictions = model.predict(img_array)

    # model = create_model()
    # load_weights(model)
    weights_path = os.path.join(settings.MEDIA_ROOT_MODEL, 'pruned_recompiled_xception_fold_1.h5')
    # print(weights_path)
    # model.load_weights(weights_path)
    model = tf.keras.models.load_model(weights_path)
    prediction = model.predict(img_array)
    
    response_data = {
        'image_url': image_name,
        'predictions': prediction.tolist()
    }
    return Response(response_data, status=200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patients_image_and_prediction(request):
    serializer = patientsImageAndPredictionSerializer(data=request.data)
    if serializer.is_valid():
        patient_image_prediction = serializer.save()
        return Response({'id': patient_image_prediction.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_by_id(request, id):
    patients = patientsImageAndPrediction.objects.filter(patient_id=id)

    if patients.exists():
        serializer = patientsImageAndPredictionSerializer(patients, many=True) 
        return Response(serializer.data, status=200)
    else:
        return Response({'error': 'Patient not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_physician_decision(request):
    serializer = PhysicianDecisionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_patients_json(request):
    normal_criteria = 'Normal'
    lsil_criteria = 'LSIL'
    hsil_criteria = 'HSIL'

    abnormal_patients_ids = patientsImageAndPrediction.objects.filter(
        Q(image_prediction=lsil_criteria) | 
        Q(image_prediction=hsil_criteria) 
    ).exclude(
        Q(image_prediction='Prediction data is missing')
    ).values_list('patient_id', flat=True).distinct()

    abnormal_patients_count = patientsDetail.objects.filter(id__in=abnormal_patients_ids).count()

    normal_patients_ids = patientsImageAndPrediction.objects.filter(
        Q(image_prediction=normal_criteria) 
    ).exclude(
        Q(image_prediction='Prediction data is missing')
    ).exclude(
        patient_id__in=abnormal_patients_ids  
    ).values_list('patient_id', flat=True).distinct()

    normal_patients_count = patientsDetail.objects.filter(id__in=normal_patients_ids).count()

    total_patients_count = patientsDetail.objects.count()

    data = {
        'normal_patients_count': normal_patients_count,
        'abnormal_patients_count': abnormal_patients_count,
        'total_patients_count': total_patients_count,
    }
    return JsonResponse(data)

@api_view(['GET'])
@permission_classes([])
def gender_count(request):
    male_count = patientsDetail.objects.filter(gender__iexact='male').count()
    female_count = patientsDetail.objects.filter(gender__iexact='female').count()
    data = {
        'male_count': male_count,
        'female_count': female_count
    }

    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_registration_trends(request):
    trends = (
        patientsDetail.objects
        .annotate(month=TruncMonth('record_date'))  
        .values('month')
        .annotate(count=Count('id')) 
        .order_by('month')  
    )

    data = [{'month': trend['month'].strftime('%Y-%m'), 'count': trend['count']} for trend in trends]
    
    return JsonResponse(data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictive_outcomes_trends(request):
    normal_criteria = 'normal'
    trends = (
        patientsImageAndPrediction.objects
        .annotate(month=TruncMonth('record_date'))
        .values('month')
        .annotate(
            normal_count=Count('id', filter=Q(image_prediction__iexact=normal_criteria)),
            abnormal_count=Count('id', filter=~(Q(image_prediction__iexact=normal_criteria)))
        )
        .order_by('month')
    )

    return JsonResponse(list(trends), safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gender_distribution_trends(request):
    trends = (
        patientsDetail.objects
        .annotate(month=TruncMonth('record_date'))
        .values('month', 'gender')
        .annotate(count=Count('id'))
        .order_by('month', 'gender')
    )

    return JsonResponse(list(trends), safe=False)

@api_view(['GET'])
@permission_classes([])
def monthly_patient_count(request, year):
    try:
        # Query to get monthly data and count by gender
        patient_data = (
            patientsDetail.objects.filter(record_date__year=year)
            .annotate(month=TruncMonth('record_date'))
            .values('month')
            .annotate(
                male_count=Count('id', filter=Q(gender='Male')),
                female_count=Count('id', filter=Q(gender='Female')),
                total_count=Count('id')
            )
            .order_by('month')
        )
        
        # Prepare the monthly response data
        monthly_data = [
            {
                "month": data['month'].strftime('%b'),
                "year": year,
                "male_count": data['male_count'],
                "female_count": data['female_count'],
                "total_count": data['total_count']
            }
            for data in patient_data
        ]
        
        # List of all months to ensure all months are represented
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Format the final response with zeroes for months that have no data
        response_data = [
            {
                "month": month,
                "year": year,
                "male_count": next((item['male_count'] for item in monthly_data if item['month'] == month), 0),
                "female_count": next((item['female_count'] for item in monthly_data if item['month'] == month), 0),
                "total_count": next((item['total_count'] for item in monthly_data if item['month'] == month), 0)
            }
            for month in months
        ]
        
        # Serialize the response data
        return Response(response_data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictions_by_month(request, year):
    predictions = (
        patientsImageAndPrediction.objects.filter(record_date__year=year)
        .annotate(month=TruncMonth('record_date'))
        .values('month')
        .annotate(prediction_count=Count('id'))
        .order_by('month')
    )

    monthly_data = [
        {"month": entry['month'].strftime("%b"), "prediction_count": entry['prediction_count']}
        for entry in predictions
    ]

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    response_data = [
        {"month": month, "prediction_count": next((item['prediction_count'] for item in monthly_data if item['month'] == month), 0)}
        for month in months
    ]

    serializer = MonthlyPredictionSerializer(response_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_count_per_institution(request):
    try:
        patient_counts = (
            patientsDetail.objects
            .values('health_institution__name')  
            .annotate(patient_count=Count('id'))
            .order_by('health_institution__name')
        )

        response_data = [
            {
                "institution": data['health_institution__name'],
                "patient_count": data['patient_count']
            }
            for data in patient_counts
        ]

        return Response(response_data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    


@api_view(['GET'])
@permission_classes([])
def new_vs_returning_patients(request):
    try:
        patient_counts = (
            patientsImageAndPrediction.objects
            .values('patient_id')
            .annotate(screening_count=Count('record_date', distinct=True))
        )
        new_patients_count = 0
        returning_patients_count = 0
        for patient in patient_counts:
            if patient['screening_count'] == 1:
                new_patients_count += 1
            else:
                returning_patients_count += 1

        response_data = {
            "new_patients": new_patients_count,
            "returning_patients": returning_patients_count
        }

        return Response(response_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

