from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == "POST":
        post = request.POST
        return render(request,"MainMenu/index.html",{"username":post["username"]})
    return render(request,"MainMenu/index.html")