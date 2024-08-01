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
        if docrequest is not None:
            Doc = int(docrequest)
        print(docrequest is not None)
        if pserrequest is not None and docrequest is None and torequest is None and fromrequest is None:
            Pser = int(pserrequest)
            queryset = Payments.objects.filter(Appointment__Pser=Pser)
        elif docrequest is not None:
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
            if int(app.Fees) != int(app.Paid):
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
            changepat = patient.objects.get(Ser=obj.Pser)
            changepat.Debts -= obj.Fees
            print(changepat.Debts)
            print(newpay)
            print(serializer.validated_data)
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
            changepat = patient.objects.get(Ser=obj.Pser)
            changepat.Debts -= paidhere
            print(changepat.Debts)
            print(newpay)
            print(serializer.validated_data)
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
        serializer = PatientSerializer(obj,data={**data,**{"Admission":datetime.strptime(data['Admission'],format).date(),"BirthDate":datetime.strptime(data['BirthDate'],format).date()}}, partial=True)
        if serializer.is_valid():
            appointmentlist = appointments.objects.filter(Pser=Ser)
            for appointment in appointmentlist:
                appointment.Aname = data['PName']
                appointment.Aphone = data['Phone']
                appointment.Atel = data['Mobile']
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
    def get_queryset(self, name=None,phone=None,rowsper=25,page=1,count=None,num=None):
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        count= self.request.query_params.get('count')
        num = self.request.query_params.get('num')
        rowsper = self.request.query_params.get('rowsper') if self.request.query_params.get('rowsper') is not None else 25
        page = self.request.query_params.get('page') if self.request.query_params.get('page') is not None else 1
        if name is not None and phone is None and num is None:
            queryset = Paginator(patient.objects.filter(PName__contains=name),rowsper)
        elif name is  None and phone is not None and num is None:
            queryset = Paginator(patient.objects.filter(Phone__contains=phone),rowsper)
        elif num is not None and name is None and phone is None:
            queryset = Paginator(patient.objects.filter(Ser=num),rowsper)
        else:
            queryset = Paginator(patient.objects.all().order_by('Ser'),rowsper)
        if count:
            return [patient(Phone=f'{queryset.num_pages}')]
        return queryset.get_page(page)
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
    def get_queryset(self, name=None,doctor=None,num=None,page=1,rowsper=25,count=None):
        name = self.request.query_params.get('name')
        doctor = self.request.query_params.get('doctor')
        num = self.request.query_params.get('num')
        getrowsper=self.request.query_params.get('rowsper')
        getpage=self.request.query_params.get('page')
        count = self.request.query_params.get('count')
        if getpage is not None:page=getpage
        if getrowsper is not None:rowsper=getrowsper
        if name is not None and doctor is None and num is None:
            queryset = Paginator(appointments.objects.filter(Aname__contains=name),rowsper)
        elif doctor is not None and name is None and num is None:
            queryset = Paginator(appointments.objects.filter(Aname__contains=doctor),rowsper)
        elif num is not None and name is None and doctor is None:
            queryset = appointments.objects.filter(Pser=num)
            return queryset
        else:
            queryset = Paginator(appointments.objects.all(),rowsper)
        if count:
            return [appointments(Pser=queryset.num_pages)]
        return queryset.get_page(page)

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

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]