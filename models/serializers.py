from rest_framework import serializers
from .models import Timesheets, ConfigSalary, leave_requests

class TimesheetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheets
        fields = ['id','date', 'time_in', 'time_out', 'description' , 'site_name', 'who_signed', 'user']

class ConfigSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigSalary
        fields = ['id','WOF', 'WFH']

class leave_requestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = leave_requests
        fields = ['id','datetime_start', 'datetime_end', 'datetime_requested', 'description', 'status', 'who_signed', 'tel', 'user']