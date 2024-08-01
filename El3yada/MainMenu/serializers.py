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
        fields = ['Aser','Pser','Aname','Arraive','Aphone','Atel','Adate','DocName','Fees','Cost','Paid','ShouldPay','Arem','DoneBy','MoneyBy']
        
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):
    Appointment_info = serializers.SerializerMethodField()
    class Meta:
        model = Payments
        fields = ['Appointment_info','Paid_Amount','Date','MoneyBy']

    def get_Appointment_info(self, obj):
        # Access the related model instance using the foreign key relationship
        related_instance = obj.Appointment
        related_info = {
            'Aser': related_instance.Aser,
            'Pser': related_instance.Pser,
            'Aname': related_instance.Aname,
            'DocName': related_instance.DocName,
            'Arem': related_instance.Arem,
            # Add more fields as needed
        }

        # Customize the information you want to include from the related model

        return related_info