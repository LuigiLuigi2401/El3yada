from user_messages import api
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from MainMenu.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from rest_framework import permissions,status,viewsets,renderers,serializers,authentication
from .serializers import *
from .forms import PatientForm, UpdatePatientForm , UpdateExtraInfo, AppointmentForm , FrontEndAppointment, PaymentForm
from datetime import date
from django.core.paginator import Paginator
from rest_framework.response import Response
from django.core import serializers
from django.http import JsonResponse,HttpResponse
import json
from datetime import datetime
from django.http import Http404
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
DEBUG=True

# Create your views here.
@user_passes_test(lambda user: user.is_superuser)
def AddUsers(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            api.success(request.user,f'Account Created For {username}!')
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
    form = PatientForm(initial = {'Ser':lastnum,'Admission':todaydate,'Debts':0})
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
    listofcolumns = list(vars(appointments).keys())[14:-3]
    listofcolumns.remove('get_Arem_display')
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
                    PatientList = PatientList[2:21]
                    print(PatientList)
    listofcolumns = list(vars(appointments).keys())[14:-3]
    listofcolumns.remove('get_Arem_display')
    listofcolumns.remove('get_DoneBy_display')
    listofcolumns.remove('get_MoneyBy_display')
    listofcolumns.remove('get_DocName_display')
    AppointmentList = []
    for count,object in enumerate(appointments.objects.filter(Pser=Ser)):
                    AppointmentList.append([])
                    for var in vars(object):
                        AppointmentList[count].append(getattr(object,var))
                    AppointmentList[count] = AppointmentList[count][2:]
    listpatientinfo = ['Patient No.','Patient Name','Patient Notes','Date of Birth','Sex','Job','Marital Status','Street','Phone Number','Mobile Phone Number','Added on']
    Plist = zip(listpatientinfo, PatientList)

    listofcolumnspayment = list(vars(Payments).keys())[7:-4]
    PaymentList = []
    for count,object in enumerate(Payments.objects.filter(Appointment__Pser=Ser)):
                    PaymentList.append([])
                    for var in vars(object):
                        print(var)
                        if var == 'Appointment_id':
                            PaymentList[count].append(appointments.objects.get(pk=object.Appointment.pk).Aser)
                        else:
                            PaymentList[count].append(getattr(object,var))
                    PaymentList[count] = PaymentList[count][2:]
   
    initialcontext = {}
    listofpatientkeys = list(vars(patient).keys())[7:-2]
    listofpatientkeys.remove('get_Sex_display')
    for x,y in zip(listofpatientkeys, PatientList):
        initialcontext[x] = y
    updateform = UpdatePatientForm(initial=initialcontext)
    extraform = UpdateExtraInfo()
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    Debts = getattr(patient.objects.get(Ser=Ser),'Debts')
    return render(request,"MainMenu/PatientView.html",{'Plist':Plist,'Paylists':PaymentList,'columnspayment':listofcolumnspayment,'lists':AppointmentList,'columns':listofcolumns,'uform':updateform,'hform':extraform,'today':today,'patnotes':Debts,'Ser':Ser})

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
    listofcolumns = list(vars(appointments).keys())[14:-3]
    listofcolumns.remove('get_Arem_display')
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
        listofcolumns = list(vars(appointments).keys())[14:-3]
        listofcolumns.remove('get_Arem_display')
        listofcolumns.remove('get_DoneBy_display')
        listofcolumns.remove('get_MoneyBy_display')
        listofcolumns.remove('get_DocName_display')
        name = request.POST.get("search")
        choice = request.POST.get("choice")
        dbchoice = request.POST.get("dbchoice")
        if choice not in ['Name','Mobile Phone Number','Doctor Name','Telephone Number'] or name == '' or dbchoice not in ['Patients',"Appointments"]:
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars,'columns':listofcolumns})
        listofvars = []
        listofvars=Search(name,choice,dbchoice,listofvars,1)
        request.session['Search'] = request.POST
        if dbchoice == 'Patients' and not choice == 'Doctor Name':
                listofcolumns = list(vars(patient).keys())[7:-2]
                listofcolumns.remove('get_Sex_display')
        format = "%Y-%m-%d"
        today = date.today().strftime(format)
        
        return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name,"columns":listofcolumns,"dbchoice":dbchoice,'today':today,'page':1})
    else:
        if request.session.has_key('Search'):
            page = 1
            if request.GET.get('page') and type(request.GET.get('page')) is int:
                if request.GET.get('page') > 0:
                    page = CheckPage(name,choice,dbchoice,page)
                else:
                    page=1
            print(page)
            listofcolumns = list(vars(appointments).keys())[14:-3]
            listofcolumns.remove('get_Arem_display')
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
            listofvars=Search(name,choice,dbchoice,listofvars,page)
            if dbchoice == 'Patients' and not choice == 'Doctor Name':
                listofcolumns = list(vars(patient).keys())[7:-2]
                listofcolumns.remove('get_Sex_display')
            format = "%Y-%m-%d"
            today = date.today().strftime(format)
            return render(request,"MainMenu/index.html",{"lists":listofvars,"choice":choice,"name":name,"columns":listofcolumns,"dbchoice":dbchoice,'today':today,'page':page})

        else:
            listofcolumns = list(vars(appointments).keys())[14:-3]
            listofcolumns.remove('get_Arem_display')
            listofcolumns.remove('get_DoneBy_display')
            listofcolumns.remove('get_MoneyBy_display')
            listofcolumns.remove('get_DocName_display')  
            listofvars = []
            format = "%Y-%m-%d"
            today = date.today().strftime(format)
            return render(request,"MainMenu/index.html",{"lists":listofvars,"columns":listofcolumns,'today':today})

    
def CheckPage(name,choice,dbchoice,page):
    if choice == 'Name':
        if dbchoice == 'Appointments':
            numpages = Paginator(appointments.objects.filter(AName__contains=name), 25).num_pages
            if page > numpages:
                page = numpages
        else:
            numpages = Paginator(patient.objects.filter(PName__contains=name), 25).num_pages
            if page > numpages:
                page = numpages  
    elif choice == 'Doctor Name' and dbchoice == 'Appointments':
        numpages = Paginator(appointments.objects.filter(DocName__contains=name), 25).num_pages
        if page > numpages:
            page = numpages
    elif choice == 'Mobile Phone Number':
        if dbchoice == 'Appointments':
            numpages = Paginator(appointments.objects.filter(Atel__contains=name), 25).num_pages
            if page > numpages:
                page = numpages
        else:
            numpages = Paginator(patient.objects.filter(Mobile__contains=name), 25).num_pages
            if page > numpages:
                page = numpages
    elif choice == 'Telephone Number':
        if dbchoice == 'Appointments':
            numpages = Paginator(appointments.objects.filter(APhone__contains=name), 25).num_pages
            if page > numpages:
                page = numpages
        else:
            numpages = Paginator(patient.objects.filter(Phone__contains=name), 25).num_pages
            if page > numpages:
                page = numpages

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
    elif choice == 'Telephone Number':
        if dbchoice == 'Appointments':
            for count,object in enumerate(Paginator(appointments.objects.filter(Aphone=name), 25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
        else:
            for count,object in enumerate(Paginator(patient.objects.filter(Phone=name), 25).get_page(page)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]

    return listofvars

@login_required
def appointmentadd(request,Ser):
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
            tempdict['Paid'] = 0
            tempdict['Per'] = appointments.objects.filter(Adate=request.POST['Adate']).count() + 1
            request.POST = tempdict
            # print(request.POST)
            form = AppointmentForm(request.POST)
            listofservices = [x['name'] for x in list(Doctor.objects.get(bakcendname=request.POST['DocName']).services.values('name'))]
            fees = int(Services.objects.get(name=request.POST['Arem']).price)
            print(fees)
            # print(form.is_valid(),not form.cleaned_data.get("Paid")==None,form.cleaned_data.get("Fees") is not None,form.cleaned_data.get("Arem") in listofservices)
            if form.is_valid() and not form.cleaned_data.get("Paid")==None and not form.cleaned_data.get("Fees")==None and form.cleaned_data.get("Arem") in listofservices and fees == int(form.cleaned_data.get("Fees")):
                if not form.cleaned_data.get("Arem").lower() == 'payment':
                    print('Success')
                    if not DEBUG:
                        form.save()
                    for user in User.objects.all():
                        doc = form.cleaned_data.get("DocName")
                        api.success(user,f'Appointment Data Created for {name}with the Service {form.cleaned_data.get("Arem")} for Doctor {[x for (y, x) in appointments.DOC_CHOICES if y == doc][0]} and Fees of {form.cleaned_data.get("Fees")} L.E.')
                    sub = int(form.cleaned_data.get("Fees"))
                    print(sub)
                    if form.cleaned_data.get("ShouldPay") == True:
                        obj = patient.objects.get(Ser=request.POST["Pser"])
                        print(obj)
                        if obj.Debts == None:
                            obj.Debts=sub
                        else:
                            obj.Debts = int(obj.Debts) + sub
                        print(obj.Debts)
                        obj.save()
                        for user in User.objects.all():
                            api.warning(user,f'Patient Debts increased to {obj.Debts}')
                    return redirect('index')
                else:
                    messages.warning(request,f'Error Occurred!')
                
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
    form = FrontEndAppointment(initial={'Aser':lastnum,'Adate':todaydate,'DoneBy':doneby,'Pser':Ser})
    format = "%Y-%m-%d"
    today = date.today().strftime(format)
    context={
        'form':form,
        'today':today
    }
    return render(request,'MainMenu/AppointmentAdd.html',context)

@login_required
def count(request,category,rowsper):
    if category=='appointments':
        return JsonResponse({'count':Paginator(appointments.objects.all(),rowsper).num_pages})
    elif category=='patients':
        return JsonResponse({'count':Paginator(patient.objects.all(),rowsper).num_pages})


@login_required
def payment(request,Pser):
    if request.method == 'POST':
        form = PaymentForm(Pser,request.POST)
        patobj = patient.objects.get(Ser=Pser)
        appobj = appointments.objects.get(pk=request.POST['Appointment'])
        paidamount = int(request.POST['Paid_Amount'])
        if appobj.Paid == None:
            subcheck = paidamount<=(appobj.Fees)
        else:
            subcheck = paidamount<=(appobj.Fees-appobj.Paid)
        # print(form.is_valid, patobj.Debts is not None, paidamount<=patobj.Debts , subcheck)
        if form.is_valid and (patobj.Debts is not None or patobj.Debts>0) and paidamount<=patobj.Debts and subcheck:
            print(patobj,appobj)
            if not DEBUG:
                form.save()
            patobj.Debts-=paidamount
            if appobj.Paid == None:
                appobj.Paid=paidamount
            else:
                appobj.Paid+=paidamount
            if appobj.Fees-appobj.Paid ==0:
                appobj.ShouldPay = False
            print(patobj,appobj,appobj.Paid,patobj.Debts,appobj.ShouldPay)
            print('success')
            for user in User.objects.all():
                api.success(user,f'Paid Amount of {paidamount} L.E Succesfully for Patient {patobj.PName}')
            if not DEBUG:
                patobj.save()
                appobj.save()
                

    form = PaymentForm(Pser)
    context={
        'form' : form
    }
    return render(request,'MainMenu/payment.html',context=context)

@method_decorator(cache_page(60 * 60), name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self,name='',num=0):
        name =  self.request.query_params.get('name')
        num =  self.request.query_params.get('num')
        if not num == 0:
            queryset = User.objects.filter(id=num)
        elif not name == '':
            queryset = User.objects.filter(username=name) 
        return queryset

@method_decorator(cache_page(60 * 60), name='dispatch')
class DoctorView(APIView):
    """
    API endpoint that allows doctors to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(Doctor.objects.first().services.all())
        # listofdocs = {{doctor.bakcendname:doctor.name}:{service.pk:f"{service.name}({service.price} L.E.)" for service in doctor.services.all()}for doctor in Doctor.objects.all()}
        dictofdocs = []
        for doctor in Doctor.objects.all():
                dictofdocs.append({
                    'name':doctor.name,
                    'services':[{
                        'id':service.pk,
                        'name':service.name,
                        'price':service.price
                    }for service in doctor.services.all()]
                })
        print(dictofdocs)
        return Response(dictofdocs,status=status.HTTP_200_OK)


@method_decorator(cache_page(60 * 60), name='dispatch')
class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """
    serializer_class = ServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self,service=None):
        queryset = Services.objects.all()
        return queryset

class PaymentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """
    serializer_class = PaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        pserrequest = self.request.query_params.get('Pser')
        docrequest = self.request.query_params.get('Doc')
        fromrequest = self.request.query_params.get('from')
        torequest = self.request.query_params.get('to')
        if pserrequest is not None and docrequest is None:
            if torequest is not None and fromrequest is not None:
                Pser = int(pserrequest)
                queryset = Payments.objects.filter(Appointment__Pser=Pser,Appointment__Adate__range=[fromrequest,torequest])
            else:
                Pser = int(pserrequest)
                queryset = Payments.objects.filter(Appointment__Pser=Pser)
        elif docrequest is not None:
            Doc = int(docrequest)
            if pserrequest is None and torequest is None and fromrequest is None:
                queryset = Payments.objects.filter(Appointment__DocName=Doctor.objects.get(pk=Doc).name)
            elif torequest is not None and fromrequest is not None:
                queryset = Payments.objects.filter(Appointment__DocName=Doctor.objects.get(pk=Doc).name,Appointment__Adate__range=[fromrequest,torequest])
        else:
            queryset = Payments.objects.all()
        print(queryset)
        return queryset
    
class AddNewAppointmentView(APIView):
    """
    API endpoint to create appointments
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        Pser=int(request.data.get('Pser'))
        serviceId=int(request.data.get('Arem'))
        pat=patient.objects.get(Ser=Pser)
        serv=Services.objects.get(pk=serviceId)
        format = "%Y-%m-%d"
        data=request.data
        print(request.data)
        data = {**data,
            **{"Aser": appointments.objects.order_by('Aser').last().Aser + 1,
            "Aname": pat.PName,
            "Aphone": pat.Phone,
            "Atel": pat.Mobile,
            "Arraive":request.data.get('Arraive'),
            "Adate":datetime.strptime(data['Adate'],format).date(),
            "Fees": serv.price,
            "Arem": serv.name,
            "Paid":0 ,
            "Cost":serv.cost,
            "ShouldPay": request.data.get('ShouldPay'),
            "MoneyBy":''
            }
        }
        print(data)
        
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            if request.data.get('ShouldPay'):
                patToUpdate = patient.objects.get(Ser=Pser)
                patToUpdate.Debts += serv.price 
                patToUpdate.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAppointmentToPayForView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = appointments.objects.filter(Pser=self.request.query_params.get('Pser'))
        listofids = []
        for app in queryset:
            if int(app.Fees) != int(app.Paid) and app.Arraive == True:
                listofids.append(app.Aser)
        queryset = queryset.filter(Aser__in=listofids)
        return queryset
        
class EditAppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, Aser):
        try:
            obj=appointments.objects.get(Aser=Aser)
        except obj.DoesNotExist:
            raise Http404
        data=request.data
        obj._action_note = f"Appointment {obj.Aser} for {obj.Aname} was edited"
        serializer = AppointmentSerializer(obj,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PayDiagnosisAppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, Aser):
        try:
            obj=appointments.objects.get(Aser=Aser)
        except obj.DoesNotExist:
            raise Http404
        data={
            'Paid':obj.Fees,
            'ShouldPay':False,
            'MoneyBy':request.data.get('username')
        }
        serializer = AppointmentSerializer(obj,data=data, partial=True)
        if serializer.is_valid():
            newpay = Payments(Appointment=obj,Paid_Amount=obj.Fees,MoneyBy=request.data.get('username'))
            newpay._action_note = f"Payment Received: {obj.Fees} L.E. for Diagnosis of {obj.Aname}"
            changepat = patient.objects.get(Ser=obj.Pser)
            changepat._action_note = f"Debts settled for Patient {changepat.PName}"
            changepat.Debts -= obj.Fees
            obj._action_note = f"Diagnosis Appointment {obj.Aser} marked as paid"
            
            newpay.save()
            changepat.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PayServiceAppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, Aser):
        try:
            obj=appointments.objects.get(Aser=Aser)
        except obj.DoesNotExist:
            raise Http404
        paidhere = request.data.get('Paid_Amount')
        listofpayments = Payments.objects.filter(Appointment__pk=obj.pk)
        listmoneyby = set()
        listmoneyby.add(request.data.get('username'))
        for pay in listofpayments:
            listmoneyby.add(pay.MoneyBy)
        data={
            'Paid':obj.Paid + paidhere,
            'ShouldPay':False if obj.Paid + paidhere == obj.Fees else True,
            'MoneyBy':' , '.join([str(elem) for elem in listmoneyby]) if obj.Paid + paidhere == obj.Fees else ''
        }
        serializer = AppointmentSerializer(obj,data=data, partial=True)
        if serializer.is_valid():
            newpay = Payments(Appointment=obj,Paid_Amount=paidhere,MoneyBy=request.data.get('username'))
            newpay._action_note = f"Payment Received: {paidhere} L.E. for Services of {obj.Aname}"
            changepat = patient.objects.get(Ser=obj.Pser)
            changepat._action_note = f"Debts reduced for Patient {changepat.PName}"
            changepat.Debts -= paidhere
            obj._action_note = f"Service Appointment {obj.Aser} payment logged"
            
            newpay.save()
            changepat.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddNewPatientView(APIView):
    def post(self,request):
        data=request.data
        obj = patient(data)
        serializer = PatientSerializer(obj)
        print(obj,serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class EditPatientView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, Ser):
        try:
            obj=patient.objects.get(Ser=Ser)
        except obj.DoesNotExist:
            raise Http404
        data=request.data
        format = "%Y-%m-%d"
        obj._action_note = f"Patient {obj.PName}'s profile was updated"
        serializer = PatientSerializer(obj,data={**data,**{"Admission":datetime.strptime(data['Admission'],format).date(),"BirthDate":datetime.strptime(data['BirthDate'],format).date()}}, partial=True)
        if serializer.is_valid():
            appointmentlist = appointments.objects.filter(Pser=Ser)
            for appointment in appointmentlist:
                appointment.Aname = data['PName']
                appointment.Aphone = data['Phone']
                appointment.Atel = data['Mobile']
                appointment._action_note = "Silenced"  # Prevent noisy alerts for bulk updates
                appointment.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddDebtsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, Ser,Aser):
        try:
            obj=patient.objects.get(Ser=Ser)
            app = appointments.objects.get(Aser=Aser)
        except obj.DoesNotExist:
            raise Http404
        serializer = PatientSerializer(obj,{'Debts':obj.Debts+app.Fees}, partial=True)
        if serializer.is_valid():
            app.Arraive = True
            app.ShouldPay = True if app.Fees > 0 else False
            app.MoneyBy = app.DoneBy if app.Fees == 0 else ''
            app._action_note = f"Patient {obj.PName} marked as Arrived for Appointment {app.Aser}"
            obj._action_note = f"Patient {obj.PName} received new Debts"
            app.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        num = self.request.query_params.get('num')
        
        queryset = patient.objects.all().order_by('Ser')
        
        if num is not None:
            queryset = queryset.filter(Ser=num)
        elif name is not None:
            queryset = queryset.filter(PName__contains=name)
        elif phone is not None:
            queryset = queryset.filter(Phone__contains=phone)
            
        return queryset
    def create(self, request):
        print(request.data)
        format = "%Y-%m-%d"
        today = date.today().strftime(format)
        default = {
            "Ser": patient.objects.last().Ser +1,
            "PName": "لا اسم",
            "PatNote": "",
            "Sex": "ذكر",
            "Mstatus": "",
            "Street": "",
            "Phone": "",
            "Mobile": "",
            "Admission": today,
            "Debts": 0
        }
        # print({**default,**request.data,**{"Ser": patient.objects.last().Ser +1}})
        serializer = PatientSerializer(data={**request.data,**{"Ser": patient.objects.last().Ser +1,"Admission":datetime.strptime(request.data['Admission'],format).date(),"BirthDate":datetime.strptime(request.data['BirthDate'],format).date()}})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Appointments to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    def get_queryset(self):
        name = self.request.query_params.get('name')
        doctor = self.request.query_params.get('doctor')
        num = self.request.query_params.get('num')
        
        queryset = appointments.objects.all().order_by('-Aser')
        
        if num is not None:
            queryset = queryset.filter(Pser=num)
        elif name is not None:
            queryset = queryset.filter(Aname__contains=name)
        elif doctor is not None:
            queryset = queryset.filter(Aname__contains=doctor)
            
        return queryset

class AppointmentDayViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Appointments to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    format = "%Y-%m-%d"
    def get_queryset(self,day=date.today().strftime(format)):
        day=self.request.query_params.get('today') if not self.request.query_params.get('today') == None else day
        queryset = appointments.objects.filter(Adate=day)
        print(day)
        return queryset

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Expenses to be viewed or edited.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Expense.objects.all().order_by('-Date')

class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all()

class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Resource.objects.all()



@method_decorator(cache_page(60 * 60), name='dispatch')
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpecializationReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        
        if not from_date or not to_date:
            return Response({"error": "from and to parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        data = []
        specializations = Specialization.objects.all()
        for spec in specializations:
            spec_total = 0
            spec_data = {
                "SpecializationName": spec.Name,
                "Doctors": []
            }
            doctors = Doctor.objects.filter(specialization=spec)
            for doc in doctors:
                doc_total = 0
                doc_data = {
                    "DoctorName": doc.name,
                    "Appointments": []
                }
                
                payments = Payments.objects.filter(Appointment__DocName=doc.name, Appointment__Adate__range=[from_date, to_date])
                
                apps_dict = {}
                for p in payments:
                    a = p.Appointment
                    if a.Aser not in apps_dict:
                        apps_dict[a.Aser] = {
                            "Aser": a.Aser,
                            "PatientName": a.Aname,
                            "Date": a.Adate.strftime("%Y-%m-%d") if a.Adate else None,
                            "PaidAmount": 0,
                            "Service": a.Arem
                        }
                    apps_dict[a.Aser]["PaidAmount"] += p.Paid_Amount
                    doc_total += p.Paid_Amount
                    spec_total += p.Paid_Amount
                
                if apps_dict:
                    doc_data["Appointments"] = list(apps_dict.values())
                    doc_data["DoctorTotal"] = doc_total
                    spec_data["Doctors"].append(doc_data)
            
            if spec_data["Doctors"]:
                spec_data["SpecializationTotal"] = spec_total
                data.append(spec_data)
                
        return Response(data, status=status.HTTP_200_OK)

from django.db.models import Sum

class FinanceReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        
        if not from_date or not to_date:
            return Response({"error": "from and to parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        appt_page = int(request.query_params.get('appt_page', 1))
        exp_page = int(request.query_params.get('exp_page', 1))
        page_size = int(request.query_params.get('page_size', 10))
            
        # 1. Gross Income (Payments)
        payments_qs = Payments.objects.filter(Date__range=[from_date, to_date])
        gross_income = payments_qs.aggregate(total=Sum('Paid_Amount'))['total'] or 0
        
        # 2. Appointment Costs
        app_qs = appointments.objects.filter(Adate__range=[from_date, to_date], Arraive=True)
        appointments_cost = app_qs.aggregate(total=Sum('Cost'))['total'] or 0
        
        # 3. Supplier / Other Expenses
        exp_qs = Expense.objects.filter(Date__range=[from_date, to_date])
        supplier_expenses = exp_qs.aggregate(total=Sum('AmountPaid'))['total'] or 0
        
        # Breakdown by Resource Type
        expenses_breakdown = []
        for res_type, type_name in Resource.ResourceType:
            type_qs = exp_qs.filter(ItemPaidFor__Type=res_type)
            type_total = type_qs.aggregate(total=Sum('AmountPaid'))['total'] or 0
            if type_total > 0:
                expenses_breakdown.append({
                    "type": res_type,
                    "name": type_name,
                    "total": type_total
                })
        
        gross_expenses = appointments_cost + supplier_expenses
        net_profit = gross_income - gross_expenses
        
        # Appointments List Pagination
        from django.core.paginator import Paginator
        
        appt_paginator = Paginator(app_qs.order_by('-Adate', '-Aser'), page_size)
        app_page_obj = appt_paginator.get_page(appt_page)
        
        appointments_list = []
        for app in app_page_obj:
            appointments_list.append({
                "Aser": app.Aser,
                "Pser": app.Pser,
                "Aname": app.Aname,
                "DocName": app.DocName,
                "Arem": app.Arem,
                "Fees": app.Fees,
                "Cost": app.Cost,
                "Paid": app.Paid,
                "Adate": app.Adate.strftime("%Y-%m-%d") if app.Adate else ""
            })

        # Expenses List Pagination
        exp_paginator = Paginator(exp_qs.order_by('-Date', '-id'), page_size)
        exp_page_obj = exp_paginator.get_page(exp_page)
        
        expenses_list = []
        for exp in exp_page_obj:
            expenses_list.append({
                "id": exp.id,
                "Supplier": exp.Supplier.Name if exp.Supplier else "",
                "Resource": exp.ItemPaidFor.Name if exp.ItemPaidFor else "",
                "Amount": exp.AmountOfItem,
                "Price": exp.Price,
                "Paid": exp.AmountPaid,
                "Date": exp.Date.strftime("%Y-%m-%d") if exp.Date else "",
                "ReceiptID": exp.ReceiptID if hasattr(exp, 'ReceiptID') else ""
            })

        data = {
            "gross_income": gross_income,
            "gross_expenses": gross_expenses,
            "net_profit": net_profit,
            "details": {
                "appointments_cost": appointments_cost,
                "supplier_expenses": supplier_expenses,
                "expenses_breakdown": expenses_breakdown,
                "appointments_list": {
                    "count": appt_paginator.count,
                    "results": appointments_list
                },
                "expenses_list": {
                    "count": exp_paginator.count,
                    "results": expenses_list
                }
            }
        }
        return Response(data, status=status.HTTP_200_OK)