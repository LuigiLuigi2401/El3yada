from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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
    return render(request,"MainMenu/index.html")
