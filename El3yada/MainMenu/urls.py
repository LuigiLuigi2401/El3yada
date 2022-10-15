from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("adduser/",views.AddUsers,name="addusers"),
    path("patient/",views.Patient,name="patient"),
]