from pyexpat import model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from broilersDetail.notebook import CLASS_NAMES
from .models import broilersDetail
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
from .models import broilersDetail
import tensorflow as tf

@api_view(['GET'])
@permission_classes([])
def fetch_broilers_api(request):
    broilers = broilersDetail.objects.all()
    serializer = BroilersDetailSerializer(broilers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_broilers_supervisor_api(request, pk):
    broilers = broilersDetail.objects.filter(farm_institution=pk)
    serializer = BroilersDetailSerializer(broilers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def fetch_broiler_api(request, pk):
    broiler = broilersDetail.objects.get(pk=pk)
    serializer = BroilersDetailSerializer(broiler)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_broiler_api(request, pk):
    broiler = broilersDetail.objects.get(pk=pk)
    serializer = BroilersDetailSerializer(broiler, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_broiler_api(request, pk):
    broiler = broilersDetail.objects.get(pk=pk)
    broiler.delete()
    return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_broiler_api(request):
    serializer = BroilersDetailSerializer(data=request.data)
    if serializer.is_valid():
        broiler = serializer.save()
        response_data = {
            'id': broiler.id,
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
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, 'wb') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # Load and preprocess image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Load the exported Keras 3 SavedModel
    model_path = r"C:\Poultry\Model\poultry1_model_tf"
    model = tf.keras.models.load_model(model_path)
    CLASS_NAMES = ["Newcastle", "Normal", "Other abnormal"]

    # Use the 'serve' signature
    infer = model.signatures["serve"]
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
    prediction = infer(input_image=img_tensor)
    prediction_array = prediction["output_0"].numpy()

    pred_index = np.argmax(prediction_array, axis=1)[0]
    pred_class = CLASS_NAMES[pred_index]

    response_data = {
        'image_url': image_name,
        'predicted_class': pred_class,
        'predictions': prediction_array.tolist()
    }
    return Response(response_data, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_broilers_image_and_prediction(request):
    serializer = BroilersImageAndPredictionSerializer(data=request.data)
    if serializer.is_valid():
        broiler_health_status = serializer.save()
        return Response({'id': broiler_health_status.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_broiler_by_id(request, id):
    broilers = broilersImageAndPrediction.objects.filter(broiler_id=id)

    if broilers.exists():
        serializer = BroilersImageAndPredictionSerializer(broilers, many=True) 
        return Response(serializer.data, status=200)
    else:
        return Response({'error': 'Broiler not found'}, status=404)

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
def count_broilers_json(request):
    Newcastle_criteria = 'Newcastle'
    Normal_criteria = 'Normal'
    Other_abnormal_criteria = 'Other abnormal' 
    abnormal_broilers_ids = broilersImageAndPrediction.objects.filter(
        Q(health_status=Newcastle_criteria) | 
        Q(health_status=Other_abnormal_criteria) 
    ).exclude(
        Q(health_status='Prediction data is missing')
    ).values_list('broiler_id', flat=True).distinct()

    abnormal_broilers_count = broilersImageAndPrediction.objects.filter(broiler_id__in=abnormal_broilers_ids).count()

    normal_broilers_ids = broilersImageAndPrediction.objects.filter(
        Q(health_status=Normal_criteria) 
    ).exclude(
        Q(health_status='Prediction data is missing')
    ).exclude(
        broiler_id__in=abnormal_broilers_ids                
    ).values_list('broiler_id', flat=True).distinct()

    normal_broilers_count = broilersImageAndPrediction.objects.filter(broiler_id__in=normal_broilers_ids).count()

    total_broilers_count = broilersImageAndPrediction.objects.count()

    data = {
        'normal_broilers_count': normal_broilers_count,
        'abnormal_broilers_count': abnormal_broilers_count,
        'total_broilers_count': total_broilers_count,
    }
    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([])
def breed_count(request):
    male_count = broilerDetail.objects.filter(breed__iexact='male').count()
    female_count = broilerDetail.objects.filter(breed__iexact='female').count()
    data = {
        'male_count': male_count,
        'female_count': female_count
    }

    return JsonResponse(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def broiler_registration_trends(request):
    trends = (
        broilerDetail.objects
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
    Normal_criteria = 'Normal'
    trends = (
        broilersImageAndPrediction.objects
        .annotate(month=TruncMonth('record_date'))
        .values('month')
        .annotate(
            normal_count=Count('id', filter=Q(health_status__iexact=Normal_criteria)),
            abnormal_count=Count('id', filter=~(Q(health_status__iexact=Normal_criteria)))
        )
        .order_by('month')
    )

    return JsonResponse(list(trends), safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def breed_distribution_trends(request):
    trends = (
        broilersDetail.objects
        .annotate(month=TruncMonth('record_date'))
        .values('month', 'breed')
        .annotate(count=Count('id'))
        .order_by('month', 'breed')
    )

    return JsonResponse(list(trends), safe=False)

@api_view(['GET'])
@permission_classes([])
def monthly_broiler_count(request, year):
    try:
        # Query to get monthly data and count by breed
        broiler_data = (
            broilersDetail.objects.filter(record_date__year=year)
            .annotate(month=TruncMonth('record_date'))
            .values('month')
            .annotate(
                male_count=Count('id', filter=Q(breed='Male')),
                female_count=Count('id', filter=Q(breed='Female')),
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
            for data in broiler_data
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
        broilersImageAndPrediction.objects.filter(record_date__year=year)
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
def broiler_count_per_institution(request):
    try:
        broiler_counts = (
            broilersDetail.objects
            .values('farm_institution__name')  
            .annotate(brroiler_count=Count('id'))
            .order_by('farm_institution__name')
        )

        response_data = [
            {
                "institution": data['farm_institution__name'],
                "broiler_count": data['broiler_count']
            }
            for data in broiler_counts
        ]

        return Response(response_data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    


@api_view(['GET'])
@permission_classes([])
def new_vs_returning_broilers(request):
    try:
        broiler_counts = (
            broilersImageAndPrediction.objects
            .values('broiler_id')
            .annotate(screening_count=Count('record_date', distinct=True))
        )
        new_broilers_count = 0
        returning_broilers_count = 0
        for broiler in broiler_counts:
            if broiler['screening_count'] == 1:
                new_broilers_count += 1
            else:
                returning_broilers_count += 1

        response_data = {
            "new_broilers": new_broilers_count,
            "returning_broilers": returning_broilers_count
        }

        return Response(response_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

