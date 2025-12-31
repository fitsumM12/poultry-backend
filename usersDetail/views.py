# IMPORT LIBRARIES
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
# from .models import usersDetail, HealthyInstitution
from usersDetail.models import usersDetail, HealthyInstitution

from .serializers import UserDetailSerializer, HealthyInstitutionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
from django.http import JsonResponse

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])  # Adjust permission as needed
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                user_serializer = UserDetailSerializer(user)
                return JsonResponse({
                    'message': 'User authenticated successfully',
                    'token': access_token,
                    'refresh_token': refresh_token,
                    'user': user_serializer.data  
                })
            else:
                return JsonResponse({'message': 'Invalid email or password'}, status=400)
        else:
            return JsonResponse({'message': 'Email or password is missing'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


# UPLOAD IMAGES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_files(request):
    uploaded_files = request.FILES.getlist('files')
    file_urls = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(settings.MEDIA_ROOT_PROFILE, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        file_urls.append(file_path)
    return Response({'file_urls': file_urls})

# FETCH USERS 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_users_api(request):
    users = usersDetail.objects.all()
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data)

# FETCH USER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_api(request, pk):
    user = usersDetail.objects.get(pk=pk)
    serializer = UserDetailSerializer(user)
    return Response(serializer.data)

# UPDATE THE USER
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_api(request, pk):
    user = usersDetail.objects.get(pk=pk)
    serializer = UserDetailSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# DELETE USER
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_api(request, pk):
    user = usersDetail.objects.get(pk=pk)
    user.delete()
    return Response(status=204)

# ADD USER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_api(request):
    serializer = UserDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# BLOCK THE USER
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def block_user_api(request, pk):
    try:
        user = usersDetail.objects.get(pk=pk)
        user.status = 'BLOCKED'
        user.save()
        return Response(status=204)
    except usersDetail.DoesNotExist:
        return Response(status=404)

# APPROVE THE USER
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def approve_user_api(request, pk):
    try:
        user = usersDetail.objects.get(pk=pk)
        user.status = 'APPROVED'
        user.save()
        return Response(status=204)
    except usersDetail.DoesNotExist:
        return Response(status=404)

@api_view(['POST'])
@permission_classes([])
def refresh_token(request):
    if 'refresh_token' in request.data:
        refresh_token_str = request.data['refresh_token']
        try:
            refresh = RefreshToken(refresh_token_str)
            new_access_token = str(refresh.access_token)
            return JsonResponse({
                'access_token': new_access_token
            })
        except Exception as e:
            return JsonResponse({'error': 'Invalid refresh token'}, status=400)
    else:
        return JsonResponse({'error': 'Refresh token not provided'}, status=400)

@api_view(['GET'])
@permission_classes([])
def get_healthy_institution_count(request):
        institution_count = HealthyInstitution.objects.count()
        return Response({'institution_count': institution_count}, status=200)
