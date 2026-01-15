from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from decimal import Decimal
from import_export.admin import ImportExportModelAdmin,ExportMixin
from import_export import resources
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

@admin.register(Resource)
class ResourcesAdmin(ImportExportModelAdmin):
    class Meta:
        model = Resource
        exclude = ('id')
        fields = '__all__'

@admin.register(Supplier)
class SuppliersAdmin(ImportExportModelAdmin):
    class Meta:
        model = Supplier
        exclude = ('id')
        fields = '__all__'

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense
        fields = ['Date','Supplier','ItemPaidFor','AmountOfItem','Price',"ReceiptID",'AmountPaid']  # Fields to include in export
        export_order = ['Date','Supplier','ItemPaidFor','AmountOfItem','Price',"ReceiptID",'AmountPaid']  # Define export column order
        export_headers = ['Date','Supplier','Resource Name','Amount','Price',"ReceiptID",'Paid']

    def dehydrate_ItemPaidFor(self, obj):
        return obj.ItemPaidFor.Name if obj.ItemPaidFor else ''
    
    def dehydrate_Supplier(self, obj):
        return obj.Supplier.Name if obj.Supplier else ''
    
    def dehydrate_Price(self, obj):
        count = obj.ItemPaidFor.Counter
        displaycounter = count[:-2] if ((count[-3] == ('s' or 'z' or 'x' or 'o')) or (count[-4:-3] == ('ch' or 'ss' or 'sh'))) else count[:-1]
        return f'{obj.Price} L.E. per {displaycounter}'
    
    def dehydrate_AmountOfItem(self, obj):
        count = obj.ItemPaidFor.Counter
        return f'{obj.AmountOfItem} {count}'

        

@admin.register(Expense)
class ExpensesAdmin(ImportExportModelAdmin):
    resource_class = ExpenseResource
    exclude = ['id','Price']
    readonly_fields = ['Priceofthing']
    
    @admin.display(description="Price")
    def Priceofthing(self, instance):
        count = instance.ItemPaidFor.Counter
        display = count[:-2] if ((count[-3] == ('s' or 'z' or 'x' or 'o')) or (count[-4:-3] == ('ch' or 'ss' or 'sh'))) else count[:-1]
        return mark_safe(f'{instance.Price} L.E. per {display}')
    
    def save_model(self, request, obj, form, change):
        obj.Price = Decimal(obj.AmountPaid / obj.AmountOfItem)
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        """ Customize exported fields to show names instead of IDs. """
        listdisplay = ['Date','Supplier','get_resource_name','get_amount','get_price',"ReceiptID",'AmountPaid']
        return listdisplay

    def get_resource_name(self, obj):
        return obj.ItemPaidFor.Name if obj.ItemPaidFor else ''
    get_resource_name.short_description = 'Resource Name'
    
    def get_price(self, obj):
        count = obj.ItemPaidFor.Counter
        displaycounter = count[:-2] if ((count[-3] == ('s' or 'z' or 'x' or 'o')) or (count[-4:-3] == ('ch' or 'ss' or 'sh'))) else count[:-1]
        return f'{obj.Price} L.E. per {displaycounter}'
    get_price.short_description = 'Price of Resource'
    
    def get_amount(self, obj):
        count = obj.ItemPaidFor.Counter
        return f'{obj.AmountOfItem} {count}'
    get_amount.short_description = 'Amount'
    
    
    
