from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from users.models import CustomUser
# Create your models here.

class Timesheets(models.Model):

    type = [
    ('normal','Normal'),
    ('backdate','Backdate'),
    ]

    status = [
    (0,'rejected'),
    (1,'pending'),
    (2,'approved')
    ]
    
    time_in = models.TimeField(null=False,default='00:00')
    time_out = models.TimeField(null=True,default='-')
    description = models.CharField(max_length=256,null=False)
    type_of_work = models.CharField(max_length=50,null=False)
    date = models.DateField(null=False)
    who_signed = models.CharField(max_length=50,null=True)
    type_sign = models.CharField(max_length=50,null=False,default=type[0][0])
    status = models.CharField(max_length=50,null=False,choices=status,default=status[1][0])
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='timesheets')

class ConfigSalary(models.Model):
    WOF = models.FloatField(null=False)
    WFH = models.FloatField(null=False)

class leave_requests(models.Model):
    status = [
    (0,'rejected'),
    (1,'pending'),
    (2,'approved')
    ]

    datetime_start = models.DateTimeField(max_length=50,null=False)
    datetime_end = models.DateTimeField(max_length=50,null=False)
    datetime_requested = models.DateTimeField(max_length=50,auto_now_add=True)
    description = models.CharField(max_length=256,null=False)
    status = models.CharField(max_length=50,null=False,choices=status,default=status[1][0])
    who_signed = models.CharField(max_length=50,null=True)
    tel = models.CharField(max_length=50,null=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='leave_requests')

class Feedbacks(models.Model):
    status = [
    (0,'wait for response'),
    (1,'we have received your message')
    ]
    datetime_send = models.DateTimeField(max_length=50)
    title = models.CharField(max_length=50,null=False)
    type = models.CharField(max_length=50,null=False)
    description = models.CharField(max_length=256,null=False)
    status = models.CharField(max_length=50,null=False,choices=status,default=status[0][0])
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='feedbacks')

