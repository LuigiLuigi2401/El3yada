from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(appointments)
class AppointmentsAdmin(ImportExportModelAdmin):
    class Meta:
        model = appointments
        exclude = ('id')
        fields = ('Aser','Pser','Aname','Aphone','Atel','Adate','ServNo','Arem','Arraive','Fees','Cost','Seen','DoneBy','Per','AMPMCode','AMPM','ContrC','MoneyBy','MoneyNo')
@admin.register(patient)
class PatientsAdmin(ImportExportModelAdmin):
    class Meta:
        model = patient
        exclude = ('id')
        fields = ('Ser','PName','BirthDate','Sex','Job','Mstatus','Street','Phone','Mobile','Admission','ContC','ContN','Ref','Co','Pro','DELT','PatNote')
# Register your models here.

@admin.register(Payments)
class PaymentsAdmin(ImportExportModelAdmin):
    class Meta:
        model = Payments
        exclude = ('id')
        fields = '__all__'

@admin.register(Doctor)
class DoctorsAdmin(ImportExportModelAdmin):
    class Meta:
        model = Doctor
        exclude = ('id')
        fields = '__all__'

@admin.register(Services)
class ServicesAdmin(ImportExportModelAdmin):
    class Meta:
        model = Services
        exclude = ('id')
        fields = '__all__'
