from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups','is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = patient
        fields = ['Ser', 'PName', 'PatNote', 'BirthDate', 'Sex','Mstatus', 'Street', 'Phone', 'Mobile', 'Admission','Debts']

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = appointments
        fields = ['Aser','Pser','Aname','Arraive','Aphone','Atel','Adate','DocName','Fees','Arem','DoneBy']
        
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'