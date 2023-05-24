from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import date
from django.utils.translation import gettext_lazy as _

class Services(models.Model):
    name= models.CharField(_("Service Name"), max_length=50)
    price = models.IntegerField(_("Service Price"),validators=[MinValueValidator(0)])
    cost = models.IntegerField(_("Service Cost"),validators=[MinValueValidator(0)])
    description = models.TextField(_("Description"),null=True,blank=True)
    def __str__(self):
        return "{0} , {1} L.E.".format(self.name,self.price)

class Doctor(models.Model):
    bakcendname=models.CharField(_("Backend Name"), max_length=50,null=True)
    name = models.CharField(_("Doctor Name"),max_length=50)
    services = models.ManyToManyField(Services, verbose_name=_("Services"))
    def __str__(self):
        return "{0} , {1}".format(self.name,self.services.name)



class appointments(models.Model):
    Aser = models.IntegerField(unique=True,null=True)
    Pser = models.IntegerField(null=True,blank=True)
    Aname = models.TextField(null=True,blank=True)
    Aphone = models.TextField(null=True,blank=True)
    Atel = models.TextField(null=True,blank=True)
    Adate = models.DateField(null=True,blank=True)
    ServNo = models.IntegerField(null=True,blank=True)
    ServiceChoice=[]
    for service in Services.objects.all():
        ServiceChoice.append((service.name,f'({service.name}) {service.price} L.E'))
    print(ServiceChoice)
    Arem = models.TextField(null=True,blank=True,choices=ServiceChoice,default=ServiceChoice[0][0])
    Arraive = models.BooleanField(null=True,blank=True,default=False)
    DocNo = models.IntegerField(null=True,blank=True)
    DOC_CHOICES = [
        ('manal', 'دكتورة منال ابو الفضل'),
        ('tamer', 'دكتور تامر الشربيني'),
        ('maged', 'د. ماجد احمد عبد الفتاح'),
        ('3elwy', 'أحمد علوي بشارة'),
        ('mona', 'د. منى أحمد أبوالفضل'),
        ('7asna2', 'دكتورة حسناء فكري'),
        ('ranya', 'دكتورة رانيا غازي'),
        ('wala2', 'دكتورة ولاء محمود فودة'),
    ]
    DoneByChoices=[]
    for user in User.objects.all():
        DoneByChoices.append((user.username,user.username))
    DocChoice=[]
    for doctor in Doctor.objects.all():
        DocChoice.append((doctor.bakcendname,doctor.name))
    admin = User.objects.first().username
    DocName = models.TextField(null=True,blank=True,choices=DocChoice,default=DocChoice[0][0])
    Fees = models.IntegerField(null=True,blank=True)
    Cost = models.IntegerField(null=True,blank=True)
    Paid = models.IntegerField(null=True,blank=True)
    ShouldPay = models.BooleanField(null=True,blank=True,default=True)
    Seen = models.BooleanField(null=True,blank=True)
    DoneBy = models.TextField(null=True,blank=True,choices=DoneByChoices,default=admin)
    Per = models.IntegerField(null=True,blank=True)
    AMPMCode = models.TextField(null=True,blank=True)
    AMPM = models.TextField(null=True,blank=True)
    ContrC = models.IntegerField(null=True,blank=True)
    MoneyBy = models.TextField(null=True,blank=True,choices=DoneByChoices,default=admin)
    MoneyNo = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return "{0}, {1}, ({2}), {3}, Fees: {4}".format(self.Aser,self.Pser,self.Aname,self.Adate,self.Fees)

class patient(models.Model):
    Ser = models.IntegerField(unique=True,null=True)
    PName = models.TextField(null=True,blank=True)
    PatNote = models.TextField(null=True,blank=True)
    BirthDate = models.DateField(null=True,blank=True)
    SEX_CHOICES=[
        ('ذكر','ذكر'),
        ('أنثى','أنثى')
    ]
    Sex = models.TextField(null=True,blank=True,choices=SEX_CHOICES,default='ذكر')
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
    def __str__(self):
        return 'payment for appointment (({0})) on {1} with {2} L.E'.format(self.Appointment,self.Date,self.Paid_Amount)
