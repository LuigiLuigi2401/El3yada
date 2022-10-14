from django.contrib import admin
from .models import appointments
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(appointments)
class AppointmentsAdmin(ImportExportModelAdmin):
    class Meta:
        model = appointments
        exclude = ('id')
        fields = ('Aser','Pser','Aname','Aphone','Atel','Adate','ServNo','Arem','Arraive','Fees','Cost','Seen','DoneBy','Per','AMPMCode','AMPM','ContrC','MoneyBy','MoneyNo')
# Register your models here.
