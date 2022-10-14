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
        if choice not in ['Name','Mobile Phone Number']:
            listofvars=[]
            return render(request,"MainMenu/index.html",{"lists":listofvars})
        print(name)
        listofvars=[]
        if choice == 'Name':
            for count,object in enumerate(appointments.objects.filter(Aname__contains=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]  
        else:
            for count,object in enumerate(appointments.objects.filter(Atel__contains=name)):
                listofvars.append([])
                for var in vars(object):
                    listofvars[count].append(getattr(object,var))
                listofvars[count] = listofvars[count][2:]
    else:  
        listofvars = []
    return render(request,"MainMenu/index.html",{"lists":listofvars})
