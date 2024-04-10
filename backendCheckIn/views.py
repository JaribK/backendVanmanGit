from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from django.contrib.auth.models import User
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes

@api_view(['POST'])
def login(req):
    user = get_object_or_404(CustomUser, username=req.data['username'])
    if not user.check_password(req.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    token = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token[0].key ,"user": serializer.data})

@api_view(['POST'])
def register(req):
    serializer = UserSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(username=req.data['username'])
        user.set_password(req.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key,"user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def token(req):
    return Response(f'passed: {req.user.email}')

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout(req):
    req.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})
