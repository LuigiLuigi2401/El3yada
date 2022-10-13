from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from MainMenu.models import appointments
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def AddUsers(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f'Account Created For {username}!')
            return redirect('login')
    form = UserCreationForm()
    return render(request,"MainMenu/AddUsers.html",{"form":form})

@login_required
def index(request):
    listofvars=[]
    for count,object in enumerate(appointments.objects.all()):
        listofvars.append([])
        for var in vars(object):
            listofvars[count].append(getattr(object,var))
        listofvars[count] = listofvars[count][2:]    
    print(listofvars)
    return render(request,"MainMenu/index.html",{"lists":listofvars})
