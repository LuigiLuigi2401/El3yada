from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from MainMenu.models import appointments,patient
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer , PatientSerializer,AppointmentSerializer
from .forms import PatientForm
import datetime


# Create your views here.
@user_passes_test(lambda user: user.is_superuser)
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
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("PName")
            messages.success(request,f'Data Created for Patient {name}')
            return redirect('index')
    lastnum = int(patient.objects.last().Ser) + 1
    date = datetime.date.today()
    form = PatientForm(initial = {'Ser':lastnum,'Admission':date})
    return render(request,"MainMenu/PatientInfo.html",{'form':form})

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

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = patient.objects.all().order_by('Ser')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Appointments to be viewed or edited.
    """
    queryset = appointments.objects.all().order_by('Aser')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]