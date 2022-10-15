from django.contrib import admin
from .models import appointments,patient
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
