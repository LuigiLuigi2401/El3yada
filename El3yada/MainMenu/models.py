from django.db import models
from pyexcel_xlsx import get_data
# data = get_data("MainMenu/App.xlsx",row_limit=5)
# data['App'] = data['App'][1:]
# print(data['App'])
# Create your models here.
class appointments(models.Model):
    Aser = models.IntegerField(unique=True,null=True)
    Pser = models.IntegerField(null=True)
    Aname = models.TextField(null=True)
    Aphone = models.TextField(null=True)
    Atel = models.TextField(null=True)
    Adate = models.DateField(null=True)
    ServNo = models.IntegerField(null=True)
    Arem = models.TextField(null=True)
    Arraive = models.BooleanField(null=True)
    DocNo = models.IntegerField(null=True)
    DocName = models.TextField(null=True)
    Fees = models.IntegerField(null=True)
    Cost = models.IntegerField(null=True)
    Seen = models.BooleanField(null=True)
    DoneBy = models.TextField(null=True)
    Per = models.IntegerField(null=True)
    AMPMCode = models.TextField(null=True)
    AMPM = models.TextField(null=True)
    ContrC = models.IntegerField(null=True)
    MoneyBy = models.TextField(null=True)
    MoneyNo = models.IntegerField(null=True)
    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.Aser,self.Pser,self.Aname,self.Adate)

