from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
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
    admin = User.objects.first().username
    DocName = models.TextField(null=True,blank=True,choices=DOC_CHOICES,default='manal')
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
        return "{0}, {1}, {2}, {3}".format(self.Aser,self.Pser,self.Aname,self.Adate)

class patient(models.Model):
    Ser = models.IntegerField(unique=True,null=True)
    PName = models.TextField(null=True,blank=True)
    BirthDate = models.DateField(null=True,blank=True)
    Sex = models.TextField(null=True,blank=True)
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
    PatNote = models.TextField(null=True,blank=True)
    def __str__(self):
        return "{0},{1},{2},{3}".format(self.Ser,self.PName,self.Mobile,self.Street)

