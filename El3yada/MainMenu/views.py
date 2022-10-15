from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from MainMenu.models import appointments,patient
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
def Patient(request):
    return render(request,"MainMenu/PatientInfo.html")

@login_required
def index(request):
    listofcolumns = list(vars(appointments).keys())[6:-2]
    if request.method == 'POST':
        name = request.POST.get("search")
        choice = request.POST.get("choice")
        dbchoice = request.POST.get("dbchoice")
        if choice not in ['Name','Mobile Phone Number','Doctor Name'] or name == '' or dbchoice not in ['Patients',"Appointments"]:
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars})
        listofvars=[]
        if dbchoice == 'Patients' and not choice == 'Doctor Name':
            listofcolumns = list(vars(patient).keys())[6:-2]
        if choice == 'Name':
            if dbchoice == 'Appointments':
                for count,object in enumerate(appointments.objects.filter(Aname__contains=name)):
                    listofvars.append([])
                    for var in vars(object):
                        listofvars[count].append(getattr(object,var))
                    listofvars[count] = listofvars[count][2:]  
            else:
                for count,object in enumerate(patient.objects.filter(PName__contains=name)):
                    listofvars.append([])
                    for var in vars(object):
                        listofvars[count].append(getattr(object,var))
                    listofvars[count] = listofvars[count][2:]  
        elif choice == 'Doctor Name' and dbchoice == 'Appointments':
            for count,object in enumerate(appointments.objects.filter(DocName__contains=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
        elif choice == 'Mobile Phone Number':
            if dbchoice == 'Appointments':
                for count,object in enumerate(appointments.objects.filter(Atel=name)):
                    listofvars.append([])
                    for var in vars(object):
                        listofvars[count].append(getattr(object,var))
                    listofvars[count] = listofvars[count][2:]
            else:
                for count,object in enumerate(patient.objects.filter(Mobile=name)):
                    listofvars.append([])
                    for var in vars(object):
                        listofvars[count].append(getattr(object,var))
                    listofvars[count] = listofvars[count][2:]
        return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name,"columns":listofcolumns,"dbchoice":dbchoice})
    else:  
        listofvars = []
    return render(request,"MainMenu/index.html",{"lists":listofvars,"columns":listofcolumns})
