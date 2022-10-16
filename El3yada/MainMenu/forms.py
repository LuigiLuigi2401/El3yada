from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from numpy import append
from .models import appointments, patient

class PatientForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = patient
        exclude = ['id','Pro','Co','DELT']
        widgets = {
            'Sex': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Mobile': Textarea(attrs={'cols': 80, 'rows': 1}),
            'PName': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Job': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Mstatus': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Street': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Phone': Textarea(attrs={'cols': 80, 'rows': 1}),
            'ContN': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Ref': Textarea(attrs={'cols': 80, 'rows': 1}),

        }
        labels={
            'PName': _('Patient Name'),
            'Ser': _('Patient Number'),
            'BirthDate':_('Date Of Birth'),
            'Mstatus':_('Marital Status'),
            'PatNote':_("Patient Notes")
        }

class UpdatePatientForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = patient
        exclude = ['id','Pro','Co','DELT','Ser']
        widgets = {
            'Sex': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Mobile': Textarea(attrs={'cols': 80, 'rows': 1}),
            'PName': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Job': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Mstatus': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Street': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Phone': Textarea(attrs={'cols': 80, 'rows': 1}),
            'ContN': Textarea(attrs={'cols': 80, 'rows': 1}),
            'Ref': Textarea(attrs={'cols': 80, 'rows': 1}),

        }
        labels={
            'PName': _('Patient Name'),
            'BirthDate':_('Date Of Birth'),
            'Mstatus':_('Marital Status'),
            'PatNote':_("Patient Notes")
        }
        


class UpdateExtraInfo(ModelForm):
    class Meta:
        model = appointments
        fields = ['Aname','Atel','Aphone']