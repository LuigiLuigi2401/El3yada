from django.contrib.auth.models import User, Group
from .models import patient,appointments
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = patient
        fields = ['Ser','PName','BirthDate']

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = appointments
        fields = ['Aser','Pser','Aname','Aphone','Atel','Adate','DocName','Fees','Arem']