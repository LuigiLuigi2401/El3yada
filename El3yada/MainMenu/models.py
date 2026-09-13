from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Specialization(models.Model):
    Name = models.CharField(_("Specialization Name"), max_length=200)

    def __str__(self):
        return self.Name


class Services(models.Model):
    name= models.CharField(_("Service Name"), max_length=50)
    price = models.IntegerField(_("Service Price"),validators=[MinValueValidator(0)])
    cost = models.IntegerField(_("Service Cost"),validators=[MinValueValidator(0)])
    description = models.TextField(_("Description"),null=True,blank=True)
    def __str__(self):
        return "{0} ({1} L.E.)".format(self.name,self.price)

class Doctor(models.Model):
    name = models.CharField(_("Doctor Name"),max_length=50)
    services = models.ManyToManyField(Services, verbose_name=_("Services"))
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    def __str__(self):
        if self.pk:
            services_names = ", ".join([service.name for service in self.services.all()])
            return "{0} , [{1}]".format(self.name, services_names)
        return self.name



class appointments(models.Model):
    Aser = models.IntegerField(unique=True,null=True)
    Pser = models.IntegerField(null=True,blank=True)
    Aname = models.TextField(null=True,blank=True)
    Aphone = models.TextField(null=True,blank=True)
    Atel = models.TextField(null=True,blank=True)
    Adate = models.DateField(null=True,blank=True)
    ServNo = models.IntegerField(null=True,blank=True)
    Arem = models.TextField(null=True,blank=True)
    Arraive = models.BooleanField(null=True,blank=True,default=False)
    DocNo = models.IntegerField(null=True,blank=True)
    admin = User.objects.first().username
    DocName = models.TextField(null=True,blank=True,default='دكتورة منال ابو الفضل')
    Fees = models.IntegerField(null=True,blank=True)
    Cost = models.IntegerField(null=True,blank=True)
    Paid = models.IntegerField(null=True,blank=True)
    ShouldPay = models.BooleanField(null=True,blank=True,default=True)
    Seen = models.BooleanField(null=True,blank=True)
    DoneBy = models.TextField(null=True,blank=True,default=admin)
    Per = models.IntegerField(null=True,blank=True)
    AMPMCode = models.TextField(null=True,blank=True)
    AMPM = models.TextField(null=True,blank=True)
    ContrC = models.IntegerField(null=True,blank=True)
    MoneyBy = models.TextField(null=True,blank=True,default=admin)
    MoneyNo = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return "{0}, {1}, ({2}), {3}, Fees: {4}".format(self.Aser,self.Pser,self.Aname,self.Adate,self.Fees)

class patient(models.Model):
    Ser = models.IntegerField(unique=True,null=True)
    PName = models.TextField(null=True,blank=True)
    PatNote = models.TextField(null=True,blank=True)
    BirthDate = models.DateField(null=True,blank=True)
    
    Sex = models.TextField(null=True,blank=True,default='ذكر')
    Job = models.TextField(null=True,blank=True)
    Mstatus = models.TextField(null=True,blank=True)
    Street = models.TextField(null=True,blank=True)
    Phone = models.TextField(null=True,blank=True)
    Mobile = models.TextField(null=True,blank=True)
    Admission = models.DateField(null=True,blank=True)
    ContC = models.IntegerField(null=True,blank=True)
    ContN = models.TextField(null=True,blank=True)
    Ref = models.TextField(null=True,blank=True)
    Co = models.TextField(null=True,blank=True)
    Pro = models.TextField(null=True,blank=True)
    DELT = models.BooleanField(null=True,blank=True)
    Debts = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return "{0},{1},{2},{3}".format(self.Ser,self.PName,self.Mobile,self.Street)

class Payments(models.Model):
    Appointment = models.ForeignKey(appointments,on_delete=models.PROTECT)
    Paid_Amount = models.IntegerField(validators=[MinValueValidator(1)])
    Date = models.DateField(default=date.today)
    MoneyBy = models.TextField(null=True,blank=True)
    def __str__(self):
        return 'payment for appointment (({0})) on {1} with {2} L.E by {3}'.format(self.Appointment,self.Date,self.Paid_Amount,self.MoneyBy)

class Resource(models.Model):
    ResourceType = [
            ("UTIL"  , "Utility Bills"),
            ("NET"   , "Internet Bill"),
            ("TEL"   , "Telephone Bill"),
            ("FDWTR" , "Food / Water Resupply"),
            ("TXC"   , "Toxic Wastes"),
            ("MRKT"  , "Marketing"),
            ("CNSM"  , "Consumables"),
            ("MOB"   , "Mobile Phone Bills"),
            ("NC"    , "Not Categorized")
        ]
    Type = models.CharField(
        _("Type of Resource"),
        max_length=5,
        choices=ResourceType,
        default=ResourceType[-1],
    )
    Name = models.CharField(_("Resource Name"),max_length=200)
    Counter = models.CharField(_("Counter"),max_length=50, default='items')
    def __str__(self):
        return '{0} of type "{1}" which is sold by {2}'.format(self.Name,self.Type,self.Counter)
    
class Supplier(models.Model):
    Name = models.TextField(_("Supplier Name"))
    def __str__(self):
        return self.Name

class Expense(models.Model):
    Supplier = models.ForeignKey(Supplier,verbose_name="Supplier",on_delete=models.PROTECT)
    ItemPaidFor = models.ForeignKey(Resource,verbose_name='Resource bought',on_delete=models.PROTECT)
    AmountOfItem = models.DecimalField(_("Amount"),decimal_places=2,max_digits=20)
    Price = models.DecimalField(_("Price of Resource"),max_digits=50,decimal_places=2,null=True)
    AmountPaid = models.DecimalField(_("Paid"),max_digits=50,decimal_places=2)
    Date = models.DateField()
    ReceiptID = models.CharField(_("ID of Receipt"), max_length=100,unique=True)    
    
    def __str__(self):
        return 'On {0}, A sum of money, which equals {1} L.E. only, was paid to {2} for {3} {4} of {5}'.format(self.Date,self.AmountPaid,self.Supplier,self.AmountOfItem,self.ItemPaidFor.Counter,self.ItemPaidFor.Name)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver([post_save, post_delete], sender=patient)
def clear_patient_cache(sender, **kwargs):
    cache.clear()

@receiver([post_save, post_delete], sender=Payments)
def clear_payments_cache(sender, **kwargs):
    cache.clear()

@receiver([post_save, post_delete], sender=Doctor)
def clear_doctor_cache(sender, **kwargs):
    cache.clear()


@receiver([post_save, post_delete], sender=appointments)
@receiver([post_save, post_delete], sender=patient)
@receiver([post_save, post_delete], sender=Payments)
@receiver([post_save, post_delete], sender=Doctor)
@receiver([post_save, post_delete], sender=Services)
def clear_cache_and_notify_admin(sender, instance, created=None, **kwargs):
    cache.clear()
    channel_layer = get_channel_layer()

    action = getattr(instance, '_action_note', None)
    if action == "Silenced":
        return
        
    if not action:
        if created is True:
            action = f"New {sender.__name__} created"
        elif created is False:
            action = f"{sender.__name__} record updated"
        else:
            action = f"{sender.__name__} record deleted"

    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'admin_alerts',
            {
                'type': 'send_notification',
                'message': f'Admin Alert: {action}'
            }
        )

