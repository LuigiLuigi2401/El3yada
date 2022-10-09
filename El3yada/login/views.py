from django.http import HttpResponse
from django.shortcuts import render
from django import forms

class NameForm(forms.Form):
    username = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class': "form-control","id" : "username"}))
class PasswordForm(forms.Form):
    password = forms.CharField(label="",max_length=20,widget=forms.PasswordInput(attrs={'class': "form-control","id" : "password"}))

# Create your views here.
def index(request):
    username = NameForm()
    password = PasswordForm()
    return render(request,"login/index.html",{'form': username,'form2':password})