import re
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
from .forms import PatientForm, UpdatePatientForm , UpdateExtraInfo, AppointmentForm , FrontEndAppointment
from datetime import date
from django.core.paginator import Paginator

DEBUG=True

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
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    return render(request,"MainMenu/AddUsers.html",{"form":form,'today':today})

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
    todaydate = date.today()
    form = PatientForm(initial = {'Ser':lastnum,'Admission':todaydate})
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    return render(request,"MainMenu/PatientAdd.html",{'form':form,'today':today})

@login_required
def viewday(request,Adate):
    if request.method == "POST":
        Aser = request.POST['name']
        # print(Aser)
        objtochange = appointments.objects.get(Aser=Aser)
        if objtochange.Arraive:
            objtochange.Arraive = False
        else:
            objtochange.Arraive = True
        objtochange.save()
    obj = appointments.objects.filter(Adate=Adate)
    listofcolumns = list(vars(appointments).keys())[10:-2]
    listofcolumns.remove('get_DoneBy_display')
    listofcolumns.remove('get_MoneyBy_display')
    listofcolumns.remove('get_DocName_display')
    listofvars=[]
    for count,object in enumerate(obj):
        listofvars.append([])
        for var in vars(object):
            listofvars[count].append(getattr(object,var))
        listofvars[count] = listofvars[count][2:]
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    return render(request,"MainMenu/ViewDay.html",{"lists":listofvars,"columns":listofcolumns,'date':Adate,'today':today})

@login_required
def PatientView(request,Ser):
    if request.method == 'POST':
        patientobj = patient.objects.get(Ser=Ser)
        appointmentobj = appointments.objects.filter(Pser=Ser)
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
                    PatientList = PatientList[2:19]
                    print(PatientList)
    listofcolumns = list(vars(appointments).keys())[10:-2]
    listofcolumns.remove('get_DoneBy_display')
    listofcolumns.remove('get_MoneyBy_display')
    listofcolumns.remove('get_DocName_display')
    AppointmentList = []
    for count,object in enumerate(appointments.objects.filter(Pser=Ser)):
                    AppointmentList.append([])
                    for var in vars(object):
                        AppointmentList[count].append(getattr(object,var))
                    AppointmentList[count] = AppointmentList[count][2:]
    listpatientinfo = ['Patient Info','Patient Name','Date of Birth','Sex','Job','Marital Status','Street','Phone Number','Mobile Phone Number','Added on']
    Plist = zip(listpatientinfo, PatientList)
    initialcontext = {}
    for x,y in zip(list(vars(patient).keys())[6:], PatientList):
        initialcontext[x] = y
    updateform = UpdatePatientForm(initial=initialcontext)
    extraform = UpdateExtraInfo()
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    return render(request,"MainMenu/PatientView.html",{'Plist':Plist,'lists':AppointmentList,'columns':listofcolumns,'uform':updateform,'hform':extraform,'today':today})

@login_required
def AppointmentView(request,Aser):
    obj = appointments.objects.get(Aser=Aser)
    if request.method == 'POST':
        tempdict = request.POST.copy()
        name = patient.objects.get(Ser=request.POST["Pser"]).PName
        phone = patient.objects.get(Ser=request.POST["Pser"]).Phone
        tel = patient.objects.get(Ser=request.POST["Pser"]).Mobile
        tempdict['Aname'] = name
        tempdict['Aphone'] = phone
        tempdict['Atel'] = tel
        tempdict['Per'] = appointments.objects.filter(Adate=request.POST['Adate']).exclude(Aser=obj.Aser).count() + 1
        request.POST = tempdict
        updateform=AppointmentForm(request.POST,instance=obj)
        if updateform.is_valid():
            if not DEBUG:
                updateform.save()
            name = updateform.cleaned_data.get("Aser")
            messages.success(request,f'Updated Data For Appointment no. {name}!')
            print('Success')
    listofcolumns = list(vars(appointments).keys())[10:-2]
    listofcolumns.remove('get_DoneBy_display')
    listofcolumns.remove('get_MoneyBy_display')
    listofcolumns.remove('get_DocName_display')
    AppointmentList = []
    for var in listofcolumns:
        AppointmentList.append(getattr(appointments.objects.get(Aser=Aser),var))
    # listpatientinfo = ['Patient Info','Patient Name','Date of Birth','Sex','Job','Marital Status','Street','Phone Number','Mobile Phone Number','Added on']
    # Plist = zip(listpatientinfo, PatientList)
    initialcontext = {}
    for x,y in zip(listofcolumns, AppointmentList):
        initialcontext[x] = y
    updateform = FrontEndAppointment(initial=initialcontext)
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    return render(request,"MainMenu/AppointmentView.html",{'list':AppointmentList,'columns':listofcolumns,'uform':updateform,'today':today})



@login_required
def index(request):
    if request.method == 'POST':
        listofcolumns = list(vars(appointments).keys())[10:-2]
        listofcolumns.remove('get_DoneBy_display')
        listofcolumns.remove('get_MoneyBy_display')
        listofcolumns.remove('get_DocName_display')
        name = request.POST.get("search")
        choice = request.POST.get("choice")
        dbchoice = request.POST.get("dbchoice")
        if choice not in ['Name','Mobile Phone Number','Doctor Name'] or name == '' or dbchoice not in ['Patients',"Appointments"]:
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars,'columns':listofcolumns})
        listofvars = []
        listofvars=Search(name,choice,dbchoice,listofvars,1)
        request.session['Search'] = request.POST
        if dbchoice == 'Patients' and not choice == 'Doctor Name':
                listofcolumns = list(vars(patient).keys())[6:-2]
        format = "%Y-%m-%d"
        today = date.today().strftime(format)
        
        return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name,"columns":listofcolumns,"dbchoice":dbchoice,'today':today})
    else:
        if request.session.has_key('Search'):
            page = 1
            if request.GET.get('page') and type(request.GET.get('page')) is int:
                page = request.GET.get('page')
            listofcolumns = list(vars(appointments).keys())[10:-2]
            listofcolumns.remove('get_DoneBy_display')
            listofcolumns.remove('get_MoneyBy_display')
            listofcolumns.remove('get_DocName_display')
            name = request.session['Search'].get("search")
            choice = request.session['Search'].get("choice")
            dbchoice = request.session['Search'].get("dbchoice")
            if choice not in ['Name','Mobile Phone Number','Doctor Name'] or name == '' or dbchoice not in ['Patients',"Appointments"]:
                listofvars=[]
                return render(request,"MainMenu/index.html",{"lists":listofvars,'columns':listofcolumns})
            listofvars = []
            listofvars=Search(name,choice,dbchoice,listofvars,request.GET.get('page'))
            if dbchoice == 'Patients' and not choice == 'Doctor Name':
                listofcolumns = list(vars(patient).keys())[6:-2]
            format = "%Y-%m-%d"
            today = date.today().strftime(format)
            return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name,"columns":listofcolumns,"dbchoice":dbchoice,'today':today})

        else:
            listofcolumns = list(vars(appointments).keys())[10:-2]
            listofcolumns.remove('get_DoneBy_display')
            listofcolumns.remove('get_MoneyBy_display')
            listofcolumns.remove('get_DocName_display')  
            listofvars = []
            format = "%Y-%m-%d"
            today = date.today().strftime(format)
            return render(request,"MainMenu/index.html",{"lists":listofvars,"columns":listofcolumns,'today':today})

    

def Search(name,choice,dbchoice,listofvars,page):
    if choice == 'Name':
        if dbchoice == 'Appointments':
            for count,object in enumerate(Paginator(appointments.objects.filter(Aname__contains=name),25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]  
        else:
            for count,object in enumerate(Paginator(patient.objects.filter(PName__contains=name), 25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]  
    elif choice == 'Doctor Name' and dbchoice == 'Appointments':
        for count,object in enumerate(Paginator(appointments.objects.filter(DocName__contains=name), 25).get_page(page)):
            listofvars.append([])
            for var in vars(object):
                listofvars[count].append(getattr(object,var))
            listofvars[count] = listofvars[count][2:]
    elif choice == 'Mobile Phone Number':
        if dbchoice == 'Appointments':
            for count,object in enumerate(Paginator(appointments.objects.filter(Atel=name), 25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
        else:
            for count,object in enumerate(Paginator(patient.objects.filter(Mobile=name), 25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
    return listofvars

@login_required
def appointmentadd(request):
    if request.method == "POST" and not request.POST["Pser"] == '':
        # print(request.POST)
        tempdict = request.POST.copy()
        try:
            name = patient.objects.get(Ser=request.POST["Pser"]).PName
            phone = patient.objects.get(Ser=request.POST["Pser"]).Phone
            tel = patient.objects.get(Ser=request.POST["Pser"]).Mobile
            tempdict['Aname'] = name
            tempdict['Aphone'] = phone
            tempdict['Atel'] = tel
            tempdict['Per'] = appointments.objects.filter(Adate=request.POST['Adate']).count() + 1
            request.POST = tempdict
            # print(request.POST)
            form = AppointmentForm(request.POST)
            if form.is_valid() and int(request.POST['Paid'])<int(request.POST['Cost']):
                print('Success')
                if not DEBUG:
                    form.save()
                messages.success(request,f'Appointment Data Created for {name}')
                sub = int(form.cleaned_data.get("Cost")) - int(form.cleaned_data.get("Paid"))
                if not sub == 0:
                    messages.warning(request,f'Patient paid {form.cleaned_data.get("Paid")} of {form.cleaned_data.get("Cost")}, {sub} remain!')
                    obj = patient.objects.get(Ser=request.POST["Pser"])
                    print(obj)
                    obj.PatNote+=f'{sub} L.E remaining\n'
                    print(obj.PatNote)
                    obj.save()

                return redirect('index')
            else:
                messages.warning(request,f'Error Occurred!')
        except patient.DoesNotExist:
            messages.warning(request,f'Error Occurred! Patient Does Not Exist!')
        
        

    lastnum = int(appointments.objects.last().Aser) + 1
    todaydate = date.today()
    if request.user.get_full_name():
        doneby = request.user.get_full_name()
    else:
        doneby = request.user.username
    form = FrontEndAppointment(initial={'Aser':lastnum,'Adate':todaydate,'DoneBy':doneby})
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    context={
        'form':form,
        'today':today
    }
    return render(request,'MainMenu/AppointmentAdd.html',context)
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
        num = self.request.query_params.get('Aser')
        if name is not None and doctor is None and num is None:
            queryset = appointments.objects.raw(f'select * from MainMenu_appointments where Aname like \'%{name}%\' order by Aser')
        elif doctor is not None and name is None and num is None:
            queryset = appointments.objects.raw(f'select * from MainMenu_appointments where DocName like \'%{doctor}%\' order by Aser')
        elif num is not None and name is None and doctor is None:
            queryset = appointments.objects.raw(f'select * from MainMenu_appointments where Aser == {num}')
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