from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True , unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_superuser = models.BooleanField(_('staff'), default=False)
    role = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_logged_in = models.BooleanField(_('logged in'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class ResetPassword(models.Model):
    email = models.CharField(max_length=200, null=True)
    token = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.token
    # //This thing creates users personalized link, that they visit and have a enter new password view in Front-End.
    def get_absolute_url(self):
        return f'/{self.token}/'
