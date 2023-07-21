from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User
    

class SmsSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)



class ProjectSerializer(serializers.Serializer):
    employeeUsername = serializers.CharField(allow_null=False, required=True)
    employerUsername = serializers.CharField(allow_null=False, required=True)
    employeeName = serializers.CharField(allow_null=False, required=True)
    employerName = serializers.CharField(allow_null=False, required=True)
    employeeSms = serializers.BooleanField(default=False)
    employerSms = serializers.BooleanField(default=False)
    connection = serializers.CharField(allow_null=True, required=False)
    checkDate = serializers.CharField(allow_null=True, required=False)
    howMeet = serializers.CharField(allow_null=True, required=False)
    state = serializers.IntegerField(default=0)
    level = serializers.CharField(allow_null=True, required=False)
    address = serializers.CharField(allow_null=True, required=False)
    floor = serializers.IntegerField(default=1)
    region = serializers.CharField(allow_null=True, required=False)
    partner = serializers.BooleanField(default=False)
    visit = serializers.BooleanField(default=False)
    inPerson = serializers.BooleanField(default=False)
    checkout = serializers.BooleanField(default=False)
    advice = serializers.BooleanField(default=False)

    

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class PartialSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=1000)
    # checkDate = serializers.DateField()
    
    class Meta:
        model = Project
        fields = ['id']


class PartialProjectSerializer(serializers.ModelSerializer):
    employerName = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'employerName', 'address']

    def get_employerName(self, obj):
        return f"{obj.employer.first_name} {obj.employer.last_name}"


class ProjectDataSerializer(serializers.ModelSerializer):
    employeeUsername = serializers.CharField(source='employee.username')
    employerUsername = serializers.CharField(source='employer.username')
    employeeSms = serializers.BooleanField(default=False)
    employerSms = serializers.BooleanField(default=False)

    class Meta:
        model = Project
        fields = [
            'employeeUsername', 'employerUsername', 'employeeSms', 'employerSms',
            'connection', 'check_date', 'how_meet', 'state', 'level',
            'address', 'floor', 'region', 'partner', 'visit', 'in_person',
            'checkout', 'immediate'
        ]


class ProjectSearchSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee_username', allow_null=False, required=True)
    employer = serializers.CharField(source='employer_username', allow_null=False, required=True)
    employee_sms = serializers.BooleanField(default=False)
    employer_sms = serializers.BooleanField(default=False)

    class Meta:
        model = Project
        fields = '__all__'
