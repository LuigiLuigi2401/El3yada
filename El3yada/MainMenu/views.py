from django.http import HttpResponse, HttpResponseRedirect
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
from .forms import PatientForm, UpdatePatientForm , UpdateExtraInfo
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
def PatientAdd(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("PName")
            messages.success(request,f'Data Created for {name}')
            return redirect('index')
    lastnum = int(patient.objects.last().Ser) + 1
    date = datetime.date.today()
    form = PatientForm(initial = {'Ser':lastnum,'Admission':date})
    return render(request,"MainMenu/PatientAdd.html",{'form':form})

@login_required
def PatientView(request,Ser):
    if request.method == 'POST':
        patientobj = patient.objects.get(Ser=Ser)
        appointmentobj = appointments.objects.filter(Pser=Ser)
        print(request.POST['Phone'])
        extraformcontext = {
            'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'],
            'Aname':request.POST['PName'],
            'Aphone':request.POST['Phone'],
            'Atel':request.POST['Mobile']
        }
        updateform=UpdatePatientForm(request.POST,instance=patientobj)
        if updateform.is_valid():
            updateform.save()
            for item in appointmentobj:
                extraform = UpdateExtraInfo(extraformcontext,instance=item)
                if extraform.is_valid():
                    extraform.save()
            name = updateform.cleaned_data.get("PName")
            messages.success(request,f'Updated Data For {name}!')
            print('Success')
    PatientList = []
    for object in patient.objects.filter(Ser=Ser):
                    for var in vars(object):
                        PatientList.append(getattr(object,var))
                    PatientList = PatientList[2:12]
    listofcolumns = list(vars(appointments).keys())[6:-2]
    AppointmentList = []
    for count,object in enumerate(appointments.objects.filter(Pser=Ser)):
                    AppointmentList.append([])
                    for var in vars(object):
                        AppointmentList[count].append(getattr(object,var))
                    AppointmentList[count] = AppointmentList[count][2:]
    listpatientinfo = ['Patient Info','Patient Name','Date of Birth','Sex','Job','Marital Status','Street','Phone Number','Mobile Phone Number','Added on']
    Plist = zip(listpatientinfo, PatientList)
    if request.method == 'GET':
        initialcontext = {}
        for x,y in zip(list(vars(patient).keys())[6:], PatientList):
            initialcontext[x] = y
        print(initialcontext)
        updateform = UpdatePatientForm(initial=initialcontext)
        extraform = UpdateExtraInfo()
    return render(request,"MainMenu/PatientView.html",{'Plist':Plist,'lists':AppointmentList,'columns':listofcolumns,'uform':updateform,'hform':extraform})


@login_required
def index(request):
    listofcolumns = list(vars(appointments).keys())[6:-2]
    if request.method == 'POST':
        name = request.POST.get("search")
        choice = request.POST.get("choice")
        dbchoice = request.POST.get("dbchoice")
        if choice not in ['Name','Mobile Phone Number','Doctor Name'] or name == '' or dbchoice not in ['Patients',"Appointments"]:
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars,'columns':listofcolumns})
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
    def get_queryset(self, name=None,doctor=None):
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = appointments.objects.raw(f'select * from MainMenu_patient where PName like \'%{name}%\' order by Ser')
        else:
            queryset = appointments.objects.all().order_by('Aser')
        return queryset

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Appointments to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    def get_queryset(self, name=None,doctor=None):
        name = self.request.query_params.get('name')
        doctor = self.request.query_params.get('doctor')
        if name is not None and doctor is None:
            queryset = appointments.objects.raw(f'select * from MainMenu_appointments where Aname like \'%{name}%\' order by Aser')
        elif doctor is not None and name is None:
            queryset = appointments.objects.raw(f'select * from MainMenu_appointments where DocName like \'%{doctor}%\' order by Aser')
        else:
            queryset = appointments.objects.all().order_by('Aser')
        return queryset
    


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]