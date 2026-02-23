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
# from .predictor import create_model, load_weights
from django.contrib.auth.decorators import login_required
# from .preprocess import circle_crop
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import broilersDetail
import tensorflow as tf
from broilersDetail.predictor import get_model, predict_image, CLASS_NAMES   # ✅ GOOD
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
    # --- FIX START: Define broiler_id immediately ---
    broiler_id = request.data.get('broiler_id') 
    
    if not broiler_id:
        return Response({'error': 'No broiler_id provided in request'}, status=400)
    # --- FIX END ---

    if 'image' not in request.FILES:
        return Response({'error': 'No image file found'}, status=400)

    # -----------------------------
    # Save uploaded file
    # -----------------------------
    image_file = request.FILES['image']
    image_name = image_file.name
    image_path = os.path.join(settings.MEDIA_ROOT_RAW, image_name)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, 'wb') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # -----------------------------
    # Load + preprocess (SAME AS TRAINING)
    # -----------------------------
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0).astype("float32")

    # ⚠️ IMPORTANT — use MobileNetV2 preprocessing
    # img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # -----------------------------
     # Predict
    # -----------------------------
    pred_class, preds = predict_image(img_array)
    confidence = float(np.max(preds))
    # --- THE FIX: SAVE TO DATABASE ---
    try:
        # Get the broiler object
        broiler_obj = broilersDetail.objects.get(id=broiler_id)
        
        # Create the prediction record
        prediction_record = broilersImageAndPrediction.objects.create(
            broiler_id=broiler_obj,
            health_status=pred_class,  # This saves "Normal" or "Newcastle"
            broiler_image=image_name,
            supervisor_id=request.user.id # Records who did the prediction
        )
    except broilersDetail.DoesNotExist:
        return Response({'error': 'Broiler not found'}, status=404)
    # ---------------------------------

    return Response({
        "image_url": image_name,
        "predicted_class": pred_class,
        "confidence": confidence,
        "predictions": preds.tolist(),
        "db_record_id": prediction_record.id
    })

    # # Predict
    # # -----------------------------
    # model = get_model()        # ✅ loads once only
    # preds = model.predict(img_array)

    # pred_index = int(np.argmax(preds, axis=1)[0])
    # pred_class = CLASS_NAMES[pred_index]
    # confidence = float(preds[0][pred_index])

    # return Response({
    #     "image_url": image_name,
    #     "predicted_class": pred_class,
    #     "confidence": confidence,
    #     "predictions": preds.tolist()
    # })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_broilers_image_and_prediction(request):
    serializer = BroilersImageAndPredictionSerializer(data=request.data)
    if serializer.is_valid():
        broiler_health_status = serializer.save()
        return Response({'id': broiler_health_status.id}, status=201)
    return Response(serializer.errors, status=400)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_broiler_by_id(request, id):
#     broilers = broilersImageAndPrediction.objects.filter(broiler_id=id)

#     if broilers.exists():
#         serializer = BroilersImageAndPredictionSerializer(broilers, many=True) 
#         return Response(serializer.data, status=200)
#     else:
#         return Response({'error': 'Broiler not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_broiler_latest_prediction(request, id):
    prediction = (
        broilersImageAndPrediction.objects
        .filter(broiler_id=id)
        .order_by('-record_date')
        # .first()
    )

    if not prediction:
        return Response({'error': 'No prediction found'}, status=404)

    serializer = BroilersImageAndPredictionSerializer(prediction, many=True)
    return Response(serializer.data)

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
    # Use __iexact to ensure "normal", "Normal", and "NORMAL" all match
    # This captures everything marked as Newcastle or Other abnormal
    abnormal_ids = broilersImageAndPrediction.objects.filter(
        Q(health_status__iexact='Newcastle') | 
        Q(health_status__iexact='Other abnormal')
    ).values_list('broiler_id', flat=True).distinct()

    abnormal_count = abnormal_ids.count()

    # This captures everything marked exactly as Normal
    normal_count = broilersImageAndPrediction.objects.filter(
        health_status__iexact='Normal'
    ).exclude(
        broiler_id__in=abnormal_ids
    ).values_list('broiler_id', flat=True).distinct().count()

    # The total comes from your main records table
    total_count = broilersDetail.objects.count()

    return JsonResponse({
        'normal_broilers_count': normal_count,
        'abnormal_broilers_count': abnormal_count,
        'total_broilers_count': total_count,
    })

@api_view(['GET'])
@permission_classes([])
def breed_count(request):
    male_count = broilersDetail.objects.filter(breed__iexact='male').count()
    female_count = broilersDetail.objects.filter(breed__iexact='female').count()
    data = {
        'male_count': male_count,
        'female_count': female_count
    }

    return JsonResponse(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def broiler_registration_trends(request):
    trends = (
        broilersDetail.objects
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

