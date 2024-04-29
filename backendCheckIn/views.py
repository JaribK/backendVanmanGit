from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, ResetPasswordEmail
from django.contrib.auth.models import User
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from django.utils import timezone
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# @api_view(['POST'])
# def login(req):
#     user = get_object_or_404(CustomUser, username=req.data['username'])
#     if not user.check_password(req.data['password']):
#         return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
#     token = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
#     return Response({'token': token[0].key ,"user": serializer.data})

@api_view(['POST'])
def login(req):
    # user = get_object_or_404(CustomUser, username=req.data['username'])

    try:
        user = CustomUser.objects.get(username=req.data['username'])
    except ObjectDoesNotExist:
        return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(req.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

    if user.is_logged_in:
        return Response({'error': 'User is already logged in'}, status=status.HTTP_409_CONFLICT)

    # Fetch current time from World Time API
    world_time_response = requests.get('https://worldtimeapi.org/api/ip')
    if world_time_response.status_code == 200:
        current_time = world_time_response.json()['datetime']
        user.last_login = current_time
    else:
        # Fallback to Django's timezone.now() if World Time API call fails
        user.last_login = timezone.now()
        
    user.is_logged_in = True
    user.save()
    
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
    req.user.is_logged_in = False
    req.user.save()
    
    req.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})

@api_view(['POST'])
def change_password(request):
    if request.method == "POST":
        serializer = ResetPasswordEmail(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Generate a unique token
            token, _ = Token.objects.get_or_create(user=user)
            
            # Generate a unique slug
            slug = uuid.uuid4().hex  # Using UUID to generate a random slug
            
            # Create an instance of ResetPassword model
            reset_password_instance = ResetPassword.objects.create(
                email=email,
                token=token.key,
                slug=slug
            )

            # Here you pass the context of things above to send them in an email
            reset_password_url = f'{settings.FRONTEND_URL}/reset-password/{slug}'

            email_content = f"""
            <html>
            <head>
              <style>
                body {{
                  font-family: Arial, sans-serif;
                  line-height: 1.6;
                }}
                .container {{
                  max-width: 600px;
                  margin: 0 auto;
                  padding: 20px;
                  background-color: #f9f9f9;
                  border: 1px solid #ccc;
                }}
                .button {{
                  display: inline-block;
                  padding: 10px 20px;
                  background-color: #007bff;
                  color: #000;
                  text-decoration: none;
                  border-radius: 5px;
                }}
              </style>
            </head>
            <body>
              <div>
                <h2>Reset Your Password</h2>
                <p>Please click the following link to reset your password:</p>
                <p><a href="{reset_password_url}">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>Regards,<br>COMPANY NAME</p>
              </div>
            </body>
            </html>
            """
            # Send the email with HTML content
            send_mail(
                'Reset Your Password',  # Subject
                '',  # Empty body (since we're using HTML content)
                'COMPANY NAME',  # Sender
                [email],  # Recipient(s)
                html_message=email_content,  # HTML content
                fail_silently=False
            )
            
            return Response({'message': 'Reset password email sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        return Response({'message': 'GET request is not supported'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

