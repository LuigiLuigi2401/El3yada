from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    if request.method == "POST":
        post = request.POST
        return render(request,"MainMenu/index.html",{"username":post["username"]})
    form = UserCreationForm()
    return render(request,"MainMenu/index.html",{"form":form})