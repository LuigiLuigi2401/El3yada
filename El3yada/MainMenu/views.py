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
    if request.method == 'POST':
        name = request.POST.get("search")
        choice = request.POST.get("choice")
        if choice not in ['Name','Mobile Phone Number','Doctor Name'] or name == '':
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars})
        listofvars=[]
        if choice == 'Name':
            for count,object in enumerate(appointments.objects.filter(Aname__contains=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]  
        elif choice == 'Doctor Name':
            for count,object in enumerate(appointments.objects.filter(DocName__contains=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
        elif choice == 'Mobile Phone Number':
            for count,object in enumerate(appointments.objects.filter(Atel=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
        return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name})
    else:  
        listofvars = []
    return render(request,"MainMenu/index.html",{"lists":listofvars})
