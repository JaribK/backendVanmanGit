from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import CustomUser, ResetPassword

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','first_name','last_name','is_superuser','role']

class ResetPasswordEmail(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = (
            'email',
        )
